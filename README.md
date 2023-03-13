# stt_auto_ls
STT 자동학습체계 구축


# docker 
pip freeze > requirements.txt

이미지 생성시 logger.py 주소 확인
이미지 생성시 main.py conf 주소 확인
이미지 생성시 main.py stt 주소 확인

docker build -t asr_connector  .  
export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_18:$LD_LIBRARY_PATH

docker save -o asr_connector.tar asr_connector:latest 


docker run -v /Users/a60156661/shbdat/:/shbdat -d -p 42303:42303 asr_connector sleep infinity
docker run  -itd --net bridge -v /Users/a60156661/shbdat/:/shbdat -v /Users/a60156661/shblog/:/shblog -v /Users/a60156661/sw/stt/asr-connector/conf/:/conf -d -p 42303:42303 asr_connector
docker run --restart="always" -itd --net bridge -v /Users/a60156661/shbdat/:/shbdat -v /Users/a60156661/shblog/:/shblog -v /Users/a60156661/sw/stt/asr-connector/conf/:/conf -d -p 42303:42303 asr_connector sleep infinity

# 개발환경
docker run --restart="always" -itd --net asrconnector --ip 10.90.0.4 -v /shbdat/:/shbdat -p 42303:42303 asr_connector


# api
uvicorn main:app --reload --host=0.0.0.0 --port=8000 --workers 20

# oracle 

docker run -d --name oracle19db  -p 1521:1521  -e ORACLE_SID=DSTMDB -e ORACLE_PDB=MONGOPDB -e ORACLE_PWD=Oracle123 banglamon/oracle193db:19.3.0-ee

docker exec -it oracle19db bash -c "source /home/oracle/.bashrc; sqlplus /nolog” 

connect sys/oracle as sysdba

select count(*) from AICOWN.AIC_DIGITADESK_CONSULT_STT;
delete from AICOWN.AIC_DIGITADESK_CONSULT_STT;

create user AICOWN identified by 1234;
grant connect, resource, dba to AICOWN;

create table AICOWN.AIC_DIGITADESK_CONSULT_STT
(
    RECORD_ID VARCHAR2(30) NOT NULL,
    RECORD_DT CHAR(8) NOT NULL,
    RECORD_TIME VARCHAR2(6) NOT NULL,
    CUSNO NUMBER(10) NOT NULL,
    RECORD_CHL VARCHAR2(30) NULL,
    CNSL_G VARCHAR2(5) NULL,
    RECORD_FILE_NM VARCHAR2(100) NULL,
    CNSL_APPKEY VARCHAR2(30) NULL,
    SANGDAM_HWNNO NUMBER(8) NULL,
    CNSL_CTNT CLOB NULL,
    RECORD_TIME_V VARCHAR2(14) NULL,
    DB_DR_TIMES_V VARCHAR2(14) NULL,
    DB_DRDT VARCHAR2(8) NULL,
    DB_DR_TIME VARCHAR2(6) NULL
)

create table AICOWN.AIC_DIGITADESK_CONSULT_STT_TEST
(
    RECORD_ID VARCHAR2(30) NOT NULL,
    RECORD_DT CHAR(8) NOT NULL
)

select TO_CHAR(SYSDATE, 'HH24MISS') from AICOWN.AIC_DIGITADESK_CONSULT_STT

# config
# local
{
    "stt_url": "http://stt.ainapidev.shinhan.com/asr/recognition/?productcod=SHB&algin=yes&transactionid=0%domain=IPCC",
    "database": {
        "url": "localhost:1521/DSTMDB",
        "user": "AICOWN",
        "password": "1234"
    },
    "watch_path": "/Users/a60156661/shbdat/rec/digital_desk",
    "request_num": "5",
    "wav_path": "/Users/a60156661/shbdat/rec/digital_desk/wav"
}
# docker 
{
    "stt_url": "http://stt.ainapidev.shinhan.com/asr/recognition/?productcod=SHB&algin=yes&transactionid=0%domain=IPCC",
    "database": {
        "url": "localhost:1521/DSTMDB",
        "user": "AICOWN",
        "password": "1234"
    },
    "watch_path": "/shbdat/rec/digital_desk",
    "request_num": "5",
    "wav_path": "/shbdat/rec/digital_desk/wav"
}