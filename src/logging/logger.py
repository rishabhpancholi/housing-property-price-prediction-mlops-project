import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Specifying logs folder path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_FOLDER_PATH = BASE_DIR / "logs"

# Function to get a logger object
def get_logger(name: str, level = logging.INFO):
    """
    Creates and configures a logger

    Args:
          name (str): Name of the logger(__name__ from the calling module).
          level(logging.level): Logging level(DBUG,INFO etc).
    """
    # Making sure the logs folder exists and creating the log file path
    LOGS_FOLDER_PATH.mkdir(parents = True, exist_ok= True)
    log_file_path = LOGS_FOLDER_PATH/f"{name}.log"

    # Create a logger with a given name
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Preventing duplicate handlers
    if logger.hasHandlers():
        return logger

    # Format of logs
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes = 1_000_000,
        backupCount = 5
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Add both handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Example usage
if __name__ == "__main__":
    logger = get_logger('logging_tester')
    logger.info('The code has started to run')

    try:
        1/0
    except ZeroDivisionError as e:
        logger.exception(f'Error occured : {e}')





