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

full_text = "test"

audio_key = "123456789"

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
    + "DHS"
    + ", "
    + meta_data[0]
    + ", "
    + "DHS"
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
    + "TO_CHAR(SYSDATE, 'YYYYMMDDHH')"
    + ", "
    + "TO_CHAR(SYSDATE, 'HH24MISS')"
    + ")"
)
print(sql_str_insert)
