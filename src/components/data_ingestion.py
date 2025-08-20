import io
import sys
import boto3
import pandas as pd
from typing import Tuple

from src.logging.logger import get_logger
from src.utils.clean_utils import clean_data
from src.utils.split_utils import split_data
from src.exceptions.exception_handler import CustomException
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

logger = get_logger('data_ingestion')

class DataIngestion:
   def __init__(self, config: DataIngestionConfig):
      """
      DataIngestion class takes DataIngestionConfig as input

      """
      self.config = config

   def ingest_clean_split(self)-> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
      """
      Method to ingest data from S3 bucket

      """
      
      logger.info("Connecting to S3") 
      s3_client = boto3.client('s3')

      logger.info("Downloading raw data from S3 bucket")
      response = s3_client.get_object(
           Bucket = self.config.bucket_name,
           Key = self.config.raw_data_key
        )

      content = response["Body"].read()
      df = pd.read_csv(io.StringIO(content.decode("utf-8")))

      logger.info("Raw data downloaded and converted into pandas dataframe")

      logger.info("Cleaning raw data")
      cleaned_df = clean_data(df)
      logger.info("Raw data cleaned")
      logger.info("Shape of cleaned data: {}".format(cleaned_df.shape))

      logger.info("Splitting data into train, val and test")
      train_df,val_df,test_df = split_data(
            cleaned_df,
            self.config.test_ratio,
            self.config.val_ratio,
            self.config.test_random_state,
            self.config.val_random_state
         )
      logger.info("Data splitted into train, val and test")

      return (train_df,val_df,test_df)
      
   def push_interim_to_remote(self, interim_dfs: Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame])-> DataIngestionArtifact:
      """
      Method to push interim data to s3 bucket

      """
      logger.info("Connecting to S3")
      s3_client = boto3.client('s3')

      logger.info("Pushing interim data to S3")
      train_df,val_df,test_df = interim_dfs
      
      for df,key in [
         (train_df, self.config.interim_train_data_key),
         (val_df, self.config.interim_val_data_key),
         (test_df, self.config.interim_test_data_key)
      ]:
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index = False)
            s3_client.put_object(
               Bucket = self.config.bucket_name,
               Key = key,
               Body = csv_buffer.getvalue()
            )
            
            logger.info(f"Pushed dataframe to S3 at key: {key}")

      return DataIngestionArtifact()


# Example usage
if __name__ == "__main__":
    try:
       config = DataIngestionConfig()
       data_ingestion = DataIngestion(config)
       interim_dfs = data_ingestion.ingest_clean_split()
       data_ingestion_artifact = data_ingestion.push_interim_to_remote(interim_dfs)
       print(data_ingestion_artifact)
    except Exception as e:
        custom_exc = CustomException(e,sys)
        logger.error(f"{custom_exc}")

    


  

