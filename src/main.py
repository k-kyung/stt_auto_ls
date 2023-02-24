import random
import time
import threading
import json
from collections import deque
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from logger import Logger
from wadog import Target

# 현재 처리중인 작업 수
work_now = 0

# logging
logger = logging.getLogger("STT")


async def llsolu_stt(file):
    global work_now
    work_now -= 1
    time.sleep(random.uniform(1, 10))
    logger.info(file)


def load_queue(queue, request_num):
    while True:
        global work_now

        if len(queue) != 0 and work_now < request_num:
            print("작업시작")
            work_now += 1
            a = queue.popleft()
            asyncio.run(llsolu_stt(a))

        else:
            time.sleep(1)


def watch_dir(watch_path, queue):
    # WatchDog 디렉토리 감시
    w = Target(watch_path, queue)
    w.run()
    logger.info("Watching Dir Start....")


if __name__ == "__main__":
    # Setting Logging
    Logger()

    # Setting Config
    try:
        with open("conf.json") as f:
            config = json.load(f)
    except:
        logger.error("Missing conf.json")

    # Setting Watching Dir
    watch_path = config["watch_path"]

    # Setting Watching Dir
    request_num = int(config["request_num"])

    # Queue 생성
    queue = deque()

    # STT 처리 Thread 생성
    stt_worker = threading.Thread(target=load_queue, args=(queue, request_num))
    stt_worker.setDaemon(True)
    stt_worker.start()

    # Dir 감시
    watch_dir(watch_path, queue)
