import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from logging import StreamHandler, getLogger, Formatter

LOGS_FOLDER_PATH = Path.cwd()/"logs"
LOGS_FOLDER_PATH.mkdir(parents=True, exist_ok=True)

def get_logger(name:str)->logging.Logger:
    """
    This function will return a logger object

    """
    LOG_FILENAME = f"{name}.log"
    LOF_FILEPATH = LOGS_FOLDER_PATH/LOG_FILENAME

    logger = getLogger(name)
    logger.setLevel("INFO")

    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    formatter = Formatter(LOG_FORMAT, DATE_FORMAT)

    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        LOF_FILEPATH,
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger

#Testing
if __name__ == "__main__":
    logger = get_logger("test")
    logger.info("Logging test successful!")



