import io
import sys
import boto3
import pandas as pd
from pathlib import Path

from src.utils.clean_utils import clean_data
from src.logging.logger import get_logger
from src.exceptions.exception_handler import CustomException
from src.entity.config_entity import ETLPipelineConfig,DataIngestionConfig

logger = get_logger('etl_pipeline')


# DataPusher class
class ETLPipeline:
    def __init__(self, config: ETLPipelineConfig):
        """
        ETLPipeline class takes ETLPipelineConfig as input

        """

        self.config = config

    def extract_data(self)-> pd.DataFrame:
        """
        Method to extract raw data from data folder

        """
        base_folder = Path(__file__).resolve().parent.parent.parent
        raw_data_path = base_folder/self.config.raw_data_path

        
        raw_df = pd.read_csv(raw_data_path)
        return raw_df

    def transform_data(self,df: pd.DataFrame)-> pd.DataFrame:
        """
        Method to transform raw data into cleaned data

        """
        cleaned_df = clean_data(df)
        return cleaned_df
        
    def load_data(self,df: pd.DataFrame)-> DataIngestionConfig:
        """
        Method to load the cleaned data into the S3 Bucket

        """
        s3_client = boto3.client('s3')

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index = False)
        s3_client.put_object(
             Bucket = self.config.bucket_name,
             Key = self.config.raw_data_key,
             Body = csv_buffer.getvalue()
            )
        
        return DataIngestionConfig()
        
# Initiate data push
if __name__ == "__main__":
    config = ETLPipelineConfig()
    etl_pipeline = ETLPipeline(config)

    try:
        logger.info("Extracting raw data from raw data path")
        raw_df = etl_pipeline.extract_data()
        logger.info("Raw data extracted")

        logger.info("Cleaning raw data")
        cleaned_df = etl_pipeline.transform_data(raw_df)
        logger.info("Raw data cleaned")

        logger.info("Pushing cleaned data to S3 bucket")
        data_ingestion_config = etl_pipeline.load_data(cleaned_df)
        logger.info("Cleaned data pushed to S3 bucket")

        print(data_ingestion_config)

    except Exception as e:
        custom_exc = CustomException(e,sys)
        logger.error(f"{custom_exc}")