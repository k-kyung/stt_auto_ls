
import src.llsolluSTT as llsolluSTT
import logging
import requests
import json
import oracledb
import cx_Oracle
from pydub import AudioSegment
from src.audio import Audio

def main():

    # Logging
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')

    # handler 생성 (stream, file)
    streamHandler = logging.StreamHandler()
    fileHandler = logging.FileHandler('./test.log')
    fileHandler.setFormatter(formatter)

    # logger instance에 handler 설정
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)

    # logger level 설정
    logger.setLevel(level=logging.DEBUG)

    # conf 읽기
    try:
        with open('conf.json') as f:
            config = json.load(f)
    except:
        logger.error("Missing conf.json")


    # Read Audio & Txt
    # result : soundFile
    logger.info('추가 개발이 필요합니다.')
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

    logger.info('Success in Converting llsollu Audio Format')


    # STT
    # result : STT TEXT
    files_customer = open(output_path_customer, 'rb')
    files_consult = open(output_path_customer, 'rb')

    upload_customer = {'file':files_customer}
    upload_consult = {'file':files_consult}

    url = config['stt_url']

    #res = requests.post(url, files = upload)

    logger.info('Success in receiving STT Text')



    # STT Text Parsing 



    logger.info('Success in Parsing Text')


    # DB Insert
    # result : OSTMDB, AIC_DIGITALDESK_CONSULT_STT
    try:
        con = cx_Oracle.connect('PINO93/xxxx@127.0.0.1/orcl')
        cur = con.cursor()
        sql_str =   'SELECT * FROM PINO93.MIG_TAB_LAYOUT'


        # execute
        cur.execute(sql_str)



        cur.close()
        con.close()

    except:
        logger.error("Can't Connect DB")





if __name__ == "__main__":
    main()

