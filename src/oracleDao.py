import oracledb
import logging
from logger import Logger

# Logging
logger = logging.getLogger("STT")


def digital_desk_insert(db_instane, audio_key, meta_data, full_text):
    try:
        user = db_instane["user"]
        password = db_instane["password"]
        dns = db_instane["url"]

        con = oracledb.connect(user=user, password=password, dsn=dns)
        cur = con.cursor()

        # Capture파일명 | Loopback파일명 | 녹취일자 | 녹취시간 | 통화시간 | 상담사 사번 | 상담사 이름 | 고객번호
        sql_str_insert = (
            "INSERT INTO AICOWN.AIC_DIGITADESK_CONSULT_STT"
            + " ("
            + "RECORD_ID, "
            + "RECORD_DT, "
            + "RECORD_TIME, "
            + "CUSNO, "
            + "RECORD_CHL, "
            + "CNSL_G, "
            + "RECORD_FILE_NM, "
            + "CNSL_APPKEY, "
            + "SANGDAM_HWNNO, "
            + "CNSL_CTNT, "
            + "RECORD_TIME_V, "
            + "DB_DR_TIMES_V, "
            + "DB_DRDT, "
            + "DB_DR_TIME"
            + ") "
            + "VALUES"
            + " ("
            + audio_key
            + ", "
            + meta_data[2]
            + ", "
            + meta_data[3]
            + ", "
            + meta_data[7]
            + ", "
            + "'DHS'"
            + ", "
            + "'DHS'"
            + ", '"
            + meta_data[0]
            + "', "
            + "'DHS'"
            + ", "
            + meta_data[5]
            + ", "
            + full_text
            + ", "
            + meta_data[2]
            + meta_data[3]
            + ", "
            + "TO_CHAR(SYSDATE, 'YYYYMMDDHH24MISS')"
            + ", "
            + "TO_CHAR(SYSDATE, 'YYYYMMDD')"
            + ", "
            + "TO_CHAR(SYSDATE, 'HH24MISS')"
            + ")"
        )

        print(1)

        # execute
        result = cur.execute(sql_str_insert)
        cur.execute("commit")
        cur.close()

        logger.info("Success in Inserting Data")

    except:
        logger.error("Can't Connect DB")
        return
