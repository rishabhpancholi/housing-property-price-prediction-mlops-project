import io
import sys
import boto3
import pandas as pd
from pathlib import Path

from src.utils.clean_utils import clean_data
from src.logging.logger import get_logger
from src.exceptions.exception_handler import CustomException
from src.entity.config_entity import DataPusherConfig
from src.entity.artifact_entity import DataPusherArtifact

logger = get_logger('data_pusher')


# DataPusher class
class DataPusher:
    def __init__(self, config: DataPusherConfig):
        """
        ETLPipeline class takes DataPusherConfig as input

        """

        self.config = config

    def extract_data(self)-> pd.DataFrame:
        """
        Method to extract raw data from data folder

        """
        logger.info("Extracting raw data from raw data path")
        base_folder = Path(__file__).resolve().parent.parent.parent
        raw_data_path = base_folder/self.config.raw_data_path

        
        raw_df = pd.read_csv(raw_data_path)
        logger.info("Raw data extracted")

        return raw_df

    def transform_data(self,df: pd.DataFrame)-> pd.DataFrame:
        """
        Method to transform raw data into cleaned data

        """
        logger.info("Cleaning raw data")
        cleaned_df = clean_data(df)
        logger.info("Raw data cleaned")

        return cleaned_df
        
    def load_data(self,df: pd.DataFrame)-> DataPusherConfig:
        """
        Method to load the cleaned data into the S3 Bucket

        """
        logger.info("Pushing cleaned data to S3 bucket")
        s3_client = boto3.client('s3')

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index = False)
        s3_client.put_object(
             Bucket = self.config.bucket_name,
             Key = self.config.raw_data_key,
             Body = csv_buffer.getvalue()
            )
        
        logger.info("Cleaned data pushed to S3 bucket")
        
        return DataPusherArtifact()
        
# Initiate data push
if __name__ == "__main__":
    config = DataPusherConfig()
    data_pusher = DataPusher(config)

    try:
        raw_df = data_pusher.extract_data()
        cleaned_df = data_pusher.transform_data(raw_df)
        data_pusher_artifact = data_pusher.load_data(cleaned_df)

        print(data_pusher_artifact)

    except Exception as e:
        custom_exc = CustomException(e,sys)
        logger.error(f"{custom_exc}")