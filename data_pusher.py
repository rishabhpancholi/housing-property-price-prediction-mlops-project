import io
import sys
import boto3
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from src.utils import clean_data
from src.logging import get_logger
from src.exception import CustomException

# Configure logger
logger = get_logger('data_pusher')

# DataPusherConfig class
@dataclass
class DataPusherConfig:
    bucket_name: str = 'housepricesbucket130256'
    data_key: str = 'data/houses.csv'
    raw_data_path:Path = Path('raw_data/houses.csv')
    database_name:str = 'housing-property-price-prediction'      
    collection_name:str = 'HouseData'

# DataPusher class
class DataPusher:
    def __init__(self, config:DataPusherConfig):
        try:
            self.config = config
            logger.info("Initiating data pusher")
        except Exception as e:
            raise CustomException(e,sys)

    def extract_and_clean(self)->pd.DataFrame:
        try:
            logger.info("Converting csv to json")
            data = pd.read_csv(self.config.raw_data_path,encoding='latin1')
            logger.info("Data cleaning started")
            data = clean_data(data)
            logger.info("Data cleaning completed")
            return data     
        except Exception as e:
            raise CustomException(e,sys)

    def insert_data_to_s3(self,data:pd.DataFrame)->int:
        try:
            logger.info("Inserting data to s3")
            client = boto3.client('s3')
            csv_buffer = io.StringIO()
            data.to_csv(csv_buffer,index=False)
            client.put_object(
                Bucket=self.config.bucket_name,
                Key=self.config.data_key,
                Body=csv_buffer.getvalue()
            )
            logger.info("Inserting data to s3 completed")
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    data_pusher = DataPusher(DataPusherConfig())
    data = data_pusher.extract_and_clean()
    length = data_pusher.insert_data_to_s3(data)



