import sys
import boto3

from src.logging.logger import get_logger
from src.exceptions.exception_handler import CustomException
from src.entity.config_entity import DataPusherConfig

logger = get_logger('data_push')

# DataPusher class
class DataPusher:

    def __init__(self, config: DataPusherConfig):
        """
        DataPusher class takes DataPusherConfig as input

        """

        self.config = config

    def push_data(self):
        """
        Method to push data to AWS S3

        """

        s3_client = boto3.client('s3')
        s3_client.upload_file(
                self.config.raw_data_path, 
                self.config.bucket_name , 
                self.config.raw_data_path
            )
        
# Initiate data push
if __name__ == "__main__":
    config = DataPusherConfig()
    data_pusher = DataPusher(config)

    try:
        logger.info("Initiating raw data push to S3")
        data_pusher.push_data()
        logger.info("Raw data pushed to S3")
    except Exception as e:
        custom_exc = CustomException(e,sys)
        logger.error(f"{custom_exc}")