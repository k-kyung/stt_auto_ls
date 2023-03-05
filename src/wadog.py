import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import deque
import logging
from logger import Logger

# Logging
logger = logging.getLogger("STT")


class Target:
    watchDir = os.getcwd()

    # watchDir에 감시하려는 디렉토리를 명시한다.

    def __init__(self, watchDir, queue):
        self.observer = Observer()  # observer객체를 만듦
        self.watchDir = watchDir
        self.queue = queue

    def run(self):
        event_handler = Handler(self.queue)
        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            logger.error("Error")
            self.observer.join()


class Handler(FileSystemEventHandler):
    # FileSystemEventHandler 클래스를 상속받음.
    # 아래 핸들러들을 오버라이드 함

    def __init__(self, queue):
        self.queue = queue

    # 파일, 디렉터리가 move 되거나 rename 되면 실행
    def on_moved(self, event):
        logger.info(event)

    def on_created(self, event):  # 파일, 디렉터리가 생성되면 실행
        logger.info(event)
        if event.is_directory:
            logger.info(event)
        else:  # not event.is_directory
            """
            Fname : 파일 이름
            Extension : 파일 확장자
            """
            Fname, Extension = os.path.splitext(os.path.basename(event.src_path))
            """
                1. zip 파일
                2. exe 파일
                3. lnk 파일
            """
            if Extension == ".txt":
                logger.info(event.src_path)
                self.queue.append(event.src_path)

    def on_deleted(self, event):  # 파일, 디렉터리가 삭제되면 실행
        logger.info(event)

    def on_modified(self, event):  # 파일, 디렉터리가 수정되면 실행
        logger.info(event)
