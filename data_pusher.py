import os
import sys
import json
import pymongo
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
    mongo_db_url:str = os.getenv('MONGO_DB_URL')
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

    def extract_clean_and_convert_to_json(self)->list:
        try:
            logger.info("Converting csv to json")
            data = pd.read_csv(self.config.raw_data_path,encoding='latin1')
            logger.info("Data cleaning started")
            data = clean_data(data)
            logger.info("Data cleaning completed")
            records = list(json.loads(data.T.to_json()).values())
            logger.info("Converting csv to json completed")
            return records       
        except Exception as e:
            raise CustomException(e,sys)

    def insert_data_to_mongodb(self,records:list)->int:
        try:
            logger.info("Inserting data to mongodb")
            client = pymongo.MongoClient(self.config.mongo_db_url)
            db = client[self.config.database_name]
            collection = db[self.config.collection_name]
            collection.insert_many(records)
            logger.info("Inserting data to mongodb completed")
            client.close()
            return len(records)
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    data_pusher = DataPusher(DataPusherConfig())
    records = data_pusher.extract_clean_and_convert_to_json()
    length = data_pusher.insert_data_to_mongodb(records)
    logger.info(f"Inserted {length} records to mongodb")




