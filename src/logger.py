import logging


class Logger:
    def __init__(self):
        # Logging
        logger = logging.getLogger("STT")
        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s"
        )

        # handler 생성 (stream, file)
        streamHandler = logging.StreamHandler()
        fileHandler = logging.FileHandler("../test.log")
        fileHandler.setFormatter(formatter)

        # logger instance에 handler 설정
        logger.addHandler(streamHandler)
        logger.addHandler(fileHandler)

        # logger level 설정
        logger.setLevel(level=logging.DEBUG)
