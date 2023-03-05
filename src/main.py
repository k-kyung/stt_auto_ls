import os
import time
import threading
import json
from collections import deque
import asyncio
import re
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from oracleDao import digital_desk_insert
import logging
from logger import Logger
from wadog import Target
from audio import Audio

# 현재 처리중인 작업 수
work_now = 0

# logging
logger = logging.getLogger("STT")


async def llsolu_stt(meta_file_path, wav_path, stt_url, db_instane):
    global work_now
    work_now -= 1

    try:
        audio_key = os.path.basename(meta_file_path)[0:-4]
        text_file_customer_name = os.path.dirname(meta_file_path)
        wma_file_customer_name = (
            text_file_customer_name + "/" + audio_key + "_Capture.wma"
        )
        wma_file_consult_name = (
            text_file_customer_name + "/" + audio_key + "_Loopback.wma"
        )

        # Meta Information
        files_meta = open(meta_file_path, "r")
        # Capture파일명 | Loopback파일명 | 녹취일자 | 녹취시간 | 통화시간 | 상담사 사번 | 상담사 이름 | 고객번호
        meta_data = files_meta.readlines()[0].split("|")

        logger.info(meta_data)

    except:
        logger.error("Error in Meta Data")
        return

    # Transfer Audio
    # result : Mono, 8000Hz, Wav File
    try:
        wma_file_customer = Audio(wma_file_customer_name)
        wma_file_consult = Audio(wma_file_consult_name)

        output_path_customer = wav_path + "/" + audio_key + "_Capture.wav"
        output_path_consult = wav_path + "/" + audio_key + "_Loopback.wav"

        wma_file_customer.convert_stereo_to_mono()
        wma_file_customer.convert_sample_rate(8000)
        wma_file_customer.export_wav(output_path_customer, "wav")

        wma_file_consult.convert_stereo_to_mono()
        wma_file_consult.convert_sample_rate(8000)
        wma_file_consult.export_wav(output_path_consult, "wav")

        logger.info("Success in Converting llsollu Audio Format")

    except:
        logger.error("Error in Converting Audio Format")
        return

    # STT
    # result : STT TEXT
    try:
        files_customer = open(output_path_customer, "rb")
        files_consult = open(output_path_consult, "rb")

        upload_customer = {"file": files_customer}
        upload_consult = {"file": files_consult}

        # res_customer = requests.post(stt_url, files=upload_customer)
        # res_consult = requests.post(stt_url, files=upload_consult)

        stt_url_a = "http://localhost:8000/asr/recognitionA/"
        stt_url_b = "http://localhost:8000/asr/recognitionB/"
        res_customer = requests.post(stt_url_a, files=upload_customer)
        res_consult = requests.post(stt_url_b, files=upload_consult)

        logger.info("Success in receiving STT Text")

    except:
        logger.error("Error in receiving STT Text")
        return

    # STT Text Parsing
    try:
        text_customer_array = res_customer.json()["result"].split("\n")
        text_consult_array = res_consult.json()["result"].split("\n")

        text_customer_array_time = []
        text_consult_array_time = []
        text_total_array_time = []

        for idx, text in enumerate(text_customer_array):
            if "|s" not in text:
                start_time = re.match(r"[0-9]+", text).group(0)
                end_time = re.search(r"\|(.+?)\|", text).group(1)
                text_raw = re.search(r"[가-힣]+", text).group(0)

                n_length = len(text_customer_array_time)

                if n_length > 0:
                    if int(text_customer_array_time[n_length - 1][1]) == int(
                        start_time
                    ):
                        text_customer_array_time[n_length - 1][2] += " " + text_raw
                        text_customer_array_time[n_length - 1][1] = end_time
                    else:
                        text_customer_array_time += [
                            [int(start_time), int(end_time), text_raw, "C"]
                        ]

                else:
                    text_customer_array_time += [
                        [int(start_time), int(end_time), text_raw, "C"]
                    ]

        for idx, text in enumerate(text_consult_array):
            if "|s" not in text:
                start_time = re.match(r"[0-9]+", text).group(0)
                end_time = re.search(r"\|(.+?)\|", text).group(1)
                text_raw = re.search(r"[가-힣]+", text).group(0)

                n_length = len(text_consult_array_time)

                if n_length > 0:
                    if int(text_consult_array_time[n_length - 1][1]) == int(start_time):
                        text_consult_array_time[n_length - 1][2] += " " + text_raw
                        text_consult_array_time[n_length - 1][1] = end_time
                    else:
                        text_consult_array_time += [
                            [int(start_time), int(end_time), text_raw, "A"]
                        ]

                else:
                    text_consult_array_time += [
                        [int(start_time), int(end_time), text_raw, "A"]
                    ]

        text_total_array_time = text_customer_array_time + text_consult_array_time
        text_total_array_time.sort(key=lambda x: x[0])

        # 앞에 같은 화자가 발화 시, 텍스트를 합쳐 최종 array로 생성
        text_total_array = []

        for idx, text in enumerate(text_total_array_time):
            start_time = text_total_array_time[idx][0]
            end_time = text_total_array_time[idx][1]
            text_raw = text_total_array_time[idx][2]
            gobun_A_C = text_total_array_time[idx][3]
            n_length = len(text_total_array)

            if n_length > 0:
                if text_total_array[n_length - 1][3] == gobun_A_C:
                    text_total_array[n_length - 1][2] += " " + text_raw
                    text_total_array[n_length - 1][1] = end_time
                else:
                    text_total_array += [
                        [int(start_time), int(end_time), text_raw, gobun_A_C]
                    ]

            else:
                text_total_array += [
                    [int(start_time), int(end_time), text_raw, gobun_A_C]
                ]

        logger.info(text_total_array)

        # Clob 타입으로 insert가 될 수 있게 full_text 생성
        full_text = ""

        clob_start_pipe = "TO_CLOB('"
        clob_end_pipe = "')"
        index_pipe = 0

        for idx in text_total_array_time:
            index_pipe += 1
            if index_pipe % 2 == 1:
                full_text += clob_start_pipe
                full_text += (
                    idx[3] + "|" + str(idx[0]) + "|" + str(idx[1]) + "|" + idx[2] + "\n"
                )
            elif index_pipe != len(text_total_array_time):
                full_text += (
                    idx[3]
                    + "|"
                    + str(idx[0])
                    + "|"
                    + str(idx[1])
                    + "|"
                    + idx[2]
                    + clob_end_pipe
                    + "|| chr(10) ||"
                    + "\n"
                )
            else:
                full_text += (
                    idx[3]
                    + "|"
                    + str(idx[0])
                    + "|"
                    + str(idx[1])
                    + "|"
                    + idx[2]
                    + clob_end_pipe
                )

        logger.info(full_text)

        logger.info("Success in Parsing Text")
    except:
        logger.info("Error in Pasring Text")
        return

    # DB Insert
    # result : OSTMDB, AIC_DIGITALDESK_CONSULT_STT
    digital_desk_insert(db_instane, audio_key, meta_data, full_text)


def load_queue(queue, request_num, wav_path, stt_url, db_instane):
    while True:
        global work_now

        if len(queue) != 0 and work_now < request_num:
            print("작업시작")
            work_now += 1
            text_file_customer_path = queue.popleft()
            asyncio.run(
                llsolu_stt(text_file_customer_path, wav_path, stt_url, db_instane)
            )

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

    # Setting Wav Dir
    wav_path = config["wav_path"]

    # Setting STT URL
    stt_url = config["stt_url"]

    # Setting DB
    db_instane = config["database"]

    # Queue 생성
    queue = deque()

    # STT 처리 Thread 생성
    stt_worker = threading.Thread(
        target=load_queue, args=(queue, request_num, wav_path, stt_url, db_instane)
    )
    stt_worker.setDaemon(True)
    stt_worker.start()

    # Dir 감시
    watch_dir(watch_path, queue)
