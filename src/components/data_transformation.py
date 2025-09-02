import io
import sys
import boto3
import joblib
import warnings
import pandas as pd
from typing import Tuple
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
warnings.filterwarnings("ignore")

from src.logging.logger import get_logger
from src.exceptions.exception_handler import CustomException
from src.utils.imputation_utils import impute_data
from src.utils.transform_utils import transform_data
from src.entity.config_entity import DataTransformationConfig       
from src.entity.artifact_entity import DataTransformationArtifact

logger = get_logger('data_transformation')

# Creating a DataTransformation Class
class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
      """
      DataTransformation class takes DataTransformationConfig as input

      """
      self.config = config

    def ingest_interim_and_transform(self)-> Tuple[Tuple[pd.DataFrame, pd.DataFrame], Pipeline, ColumnTransformer]:
       """
       Method to ingest interim data and transform 

       """
       logger.info("Connecting to S3") 
       s3_client = boto3.client('s3')

       logger.info("Ingesting train and test df from S3 bucket")
       interim_dfs = []
       for key in [
            self.config.interim_train_data_key,
            self.config.interim_test_data_key
        ]:
            response = s3_client.get_object(
                Bucket = self.config.bucket_name,
                Key = key
            )

            content = response["Body"].read()
            df = pd.read_csv(io.StringIO(content.decode("utf-8")))
            interim_dfs.append(df)

       interim_dfs = tuple(interim_dfs)
       logger.info("Converted train and test to pandas dataframes")

       logger.info("Applying imputation on train and test dataframes")
       train_df, test_df, imputation_pipeline = impute_data(interim_dfs)
       imputed_dfs = (train_df, test_df)
       logger.info("Successfully imputed train and test dataframes")

       logger.info("Applying transformation on train and test dataframes")
       train_df, test_df, column_transformer = transform_data(imputed_dfs)
       preprocessed_dfs = (train_df, test_df)
       logger.info("Successfully transformed train and test dataframes")

       return (preprocessed_dfs, imputation_pipeline, column_transformer)
    
    def push_preprocessed_to_s3(self, preprocessed_dfs: Tuple[pd.DataFrame, pd.DataFrame]):
        """
        Method to push train and test data to S3 bucket

        """
        train_df, test_df = preprocessed_dfs

        logger.info("Connecting to S3") 
        s3_client = boto3.client('s3')

        logger.info("Pushing train and test df to S3 bucket")
        for key,df in [
            (self.config.preprocessed_train_data_key, train_df),
            (self.config.preprocessed_test_data_key, test_df)
        ]:
            
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index = False)
            s3_client.put_object(
                Bucket = self.config.bucket_name,
                Key = key,
                Body = csv_buffer.getvalue()
            )
        logger.info("Pushed train and test to S3 bucket")

    def push_pipeline_and_column_transformer_to_s3(self, imputation_pipeline: Pipeline, column_transformer: ColumnTransformer)->DataTransformationArtifact:
        """
        Method to push imputation pipeline and column transformer to S3 bucket

        """
        logger.info("Connecting to S3") 
        s3_client = boto3.client('s3')

        logger.info("Pushing imputation pipeline and column transformer to S3 bucket")
        for key,object in [
           (self.config.imputation_pipeline_key, imputation_pipeline),
           (self.config.column_transformer_key, column_transformer)
        ]:
            
            joblib_buffer = io.BytesIO()
            joblib.dump(object, joblib_buffer)
            s3_client.put_object(
                Bucket = self.config.bucket_name,
                Key = key,
                Body = joblib_buffer.getvalue()
            )
        logger.info("Pushed imputation pipeline and column transformer to S3 bucket")

        return DataTransformationArtifact()


# Example usage
if __name__ == "__main__":
   try:
        config = DataTransformationConfig()
        data_transformation = DataTransformation(config)
        preprocessed_dfs, imputation_pipeline, column_transformer = data_transformation.ingest_interim_and_transform()
        data_transformation.push_preprocessed_to_s3(preprocessed_dfs)
        data_transformation_artifact = data_transformation.push_pipeline_and_column_transformer_to_s3(imputation_pipeline, column_transformer)
        print(data_transformation_artifact)
   except Exception as e:
        custom_exp = CustomException(e,sys)
        logger.error(f"{custom_exp}")