import sys
import pymongo
import pandas as pd

from src.logging import get_logger
from src.utils import train_test_split
from src.exception import CustomException
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

# Configure logger
logger = get_logger('data_ingestion')

# DataIngestion class
class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)

    def export_collection_as_dataframe(self)->pd.DataFrame:
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            mongo_db_url = self.data_ingestion_config.mongo_db_url

            logger.info("Exporting collection as dataframe")
            self.mongo_client = pymongo.MongoClient(mongo_db_url)
            collection = self.mongo_client[database_name][collection_name]
            count = collection.count_documents({})
            logger.info(f"Collection '{collection_name}' in DB '{database_name}' has {count} documents")
            df = pd.DataFrame(list(collection.find()))
            logger.info("Exporting collection as dataframe completed")

            return df
        except Exception as e:
            raise CustomException(e,sys)

    def export_data_to_feature_store(self,df: pd.DataFrame)->pd.DataFrame:
        try:
            logger.info("Exporting data to feature store")
            feature_store_path = self.data_ingestion_config.feature_store_path
            feature_store_path.parent.mkdir(parents=True,exist_ok=True)
            df.to_csv(feature_store_path,index=False,header=True)
            logger.info("Exporting data to feature store completed")

            return df
        except Exception as e:
            raise CustomException(e,sys)

    def split_data_as_train_test(self,df: pd.DataFrame):
        try:
            logger.info("Splitting data as train and test")
            train_df,test_df = train_test_split(
                df,test_ratio=self.data_ingestion_config.train_test_split_ratio
            )
            logger.info("Splitting data as train and test completed")

            logger.info("Exporting train and test data to respective file paths")
            train_file_path = self.data_ingestion_config.training_file_path
            train_file_path.parent.mkdir(parents=True,exist_ok=True)
            train_df.to_csv(
                train_file_path,index=False,header=True
            )

            test_file_path = self.data_ingestion_config.testing_file_path
            test_file_path.parent.mkdir(parents=True,exist_ok=True)
            test_df.to_csv(
                test_file_path,index=False,header=True
            )
            logger.info("Exporting train and test data to respective file paths completed")
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logger.info("Initiating data ingestion")
            df = self.export_collection_as_dataframe()
            df = self.export_data_to_feature_store(df)
            self.split_data_as_train_test(df)
            logger.info("Data ingestion completed")

            data_ingestion_artifact = DataIngestionArtifact(
                feature_store_path=self.data_ingestion_config.feature_store_path,
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)

    


