import logging
import requests
import json
import oracledb
import cx_Oracle
import re
from logger import Logger
from pydub import AudioSegment
from audio import Audio

# Logging
logger = logging.getLogger("stt")


def main():
    # conf 읽기
    try:
        with open("conf.json") as f:
            config = json.load(f)
    except:
        logger.error("Missing conf.json")

    # Read Audio & Txt
    # result : soundFile
    logger.info("추가 개발이 필요합니다.")
    wma_file_customer_name = "sample4.wma"
    wma_file_consult_name = "consult.wma"

    # Transfer Audio
    # result : Mono, 8000Hz, Wav File
    wma_file_customer = Audio(wma_file_customer_name)
    wma_file_consult = Audio(wma_file_consult_name)

    output_path_customer = "./" + wma_file_customer_name[0:-4] + ".wav"
    output_path_consult = "./" + wma_file_consult_name[0:-4] + ".wav"

    wma_file_customer.convert_stereo_to_mono()
    wma_file_customer.convert_sample_rate(8000)
    wma_file_customer.export_wav(output_path_customer, "wav")

    wma_file_consult.convert_stereo_to_mono()
    wma_file_consult.convert_sample_rate(8000)
    wma_file_consult.export_wav(output_path_consult, "wav")

    logger.info("Success in Converting llsollu Audio Format")

    # STT
    # result : STT TEXT
    files_customer = open(output_path_customer, "rb")
    files_consult = open(output_path_customer, "rb")

    upload_customer = {"file": files_customer}
    upload_consult = {"file": files_consult}

    url = config["stt_url"]

    # res_customer = requests.post(url, files = upload_customer)
    # res_consult = requests.post(url, files = upload_consult)

    logger.info("Success in receiving STT Text")

    # STT Text Parsing
    # text_customer_array = res_customer.json()['result'].split('\n')
    # text_consult_array = res_consult.json()['result'].split('\n')

    text_customer_array = [
        "0|1528|s",
        "1548|1626|안녕하세요",
        "1656|1686|데스크",
        "1686|1986|입니다",
    ]
    text_consult_array = ["0|1532|좋은", "1600|1626|아침", "1626|1886|입니다"]

    text_customer_array_time = []
    text_consult_array_time = []
    text_total_array_time = []
    full_text = ""

    for idx, text in enumerate(text_customer_array):
        if "|s" not in text:
            start_time = re.match(r"[0-9]+", text).group(0)
            end_time = re.search(r"\|(.+?)\|", text).group(1)
            text_raw = re.search(r"[가-힣]+", text).group(0)

            n_length = len(text_customer_array_time)

            if n_length > 0:
                if int(text_customer_array_time[n_length - 1][1]) == int(start_time):
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

    print(text_total_array_time)

    for idx in text_total_array_time:
        full_text += idx[3] + "|" + str(idx[0]) + "|" + str(idx[1]) + "|" + idx[2] + ">"

    print(full_text)

    logger.info("Success in Parsing Text")

    # DB Insert
    # result : OSTMDB, AIC_DIGITALDESK_CONSULT_STT
    try:
        con = cx_Oracle.connect("PINO93/xxxx@127.0.0.1/orcl")
        cur = con.cursor()
        sql_str = "SELECT * FROM PINO93.MIG_TAB_LAYOUT"

        # execute
        cur.execute(sql_str)

        cur.close()
        con.close()

    except:
        logger.error("Can't Connect DB")


if __name__ == "__main__":
    Logger()
    main()
