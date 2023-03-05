import json
import oracledb

meta_data = [
    "123456789_Capture.wma",
    "123456789_Loopback.wma",
    "20230302",
    "000000",
    "15600",
    "21101655",
    "조치형",
    "21101655",
]

full_text = """TO_CLOB('C|3288|3612|예 안녕하세요 디지털 데스크 조치형 선임 입니다
A|3660|3699|예')|| chr(10) ||
TO_CLOB('A|3702|3789|안녕하세요
C|3786|3828|아 네')|| chr(10) ||
TO_CLOB('C|3831|3993|조치형 고객님 맞으세요
A|4014|4068|네네')|| chr(10) ||
TO_CLOB('C|4114|4161|본인확인
C|4164|4254|때문에 마스크')|| chr(10) ||
TO_CLOB('C|4257|4299|잠시만
C|4302|4380|내려주시고')|| chr(10) ||
TO_CLOB('C|4383|4530|화면 한번만 봐주세요
A|4899|4923|예')|| chr(10) ||
TO_CLOB('A|4926|5022|다름이 아니라
A|5028|5076|제가 지금')|| chr(10) ||
TO_CLOB('A|5085|5205|퇴직연금
A|5253|5370|해약하고')"""

audio_key = "123456789"


with open("conf.json") as f:
    config = json.load(f)

db_instane = config["database"]

user = db_instane["user"]
password = db_instane["password"]
dns = db_instane["url"]

con = oracledb.connect(user=user, password=password, dsn=dns)
cur = con.cursor()

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
print(sql_str_insert)

sql_str_insert = "select * from AICOWN.AIC_DIGITADESK_CONSULT_STT"

# execute
result = cur.execute(sql_str_insert)
out_data = cur.fetchone()
print(out_data)
cur.execute("commit")

cur.close()

# (RECORD_ID, RECORD_DT, RECORD_TIME, CUSNO, RECORD_CHL, CNSL_G, RECORD_FILE_NM, CNSL_APPKEY, SANGDAM_HWNNO, CNSL_CTNT, RECORD_TIME_V, DB_DR_TIMES_V, DB_DRDT, DB_DR_TIME)
