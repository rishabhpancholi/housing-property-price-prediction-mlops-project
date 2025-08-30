import io
import sys
import yaml
import boto3
import joblib
import pandas as pd
from typing import Tuple

from src.logging.logger import get_logger
from src.exceptions.exception_handler import CustomException
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact
from src.utils.train_utils import train_and_evaluate
from src.utils.compare_utils import give_best_model

logger = get_logger('model_trainer')

# Loading params
with open("params.yaml","r") as f:
    params = yaml.safe_load(f)


# Creating a ModelTrainer Class
class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
      """
      ModelTrainer class takes ModelTrainerConfig as input

      """
      self.config = config

    def ingest_preprocessed(self)-> Tuple[pd.DataFrame, pd.DataFrame]:
       """
       Method to ingest preprocessed data from S3

       """
       logger.info("Connecting to S3") 
       s3_client = boto3.client('s3')

       logger.info("Ingesting preprocessed train and test df from S3 bucket")
       preprocessed_dfs = []
       for key in [
            self.config.preprocessed_train_data_key,
            self.config.preprocessed_test_data_key
        ]:
            response = s3_client.get_object(
                Bucket = self.config.bucket_name,
                Key = key
            )

            content = response["Body"].read()
            df = pd.read_csv(io.StringIO(content.decode("utf-8")))
            preprocessed_dfs.append(df)

       return tuple(preprocessed_dfs)
       
    def train_evaluate_and_register(self, preprocessed_dfs: Tuple[pd.DataFrame, pd.DataFrame])-> ModelTrainerArtifact:
        """
        Method to train the model and evaluate and register on Mlflow.

        """
        logger.info("Starting model training")
        model_pipeline = train_and_evaluate(
            mlflow_tracking_uri = self.config.mlflow_tracking_uri,
            repo_owner = self.config.repo_owner,
            repo_name = self.config.repo_name,
            regressor_name = self.config.regressor,
            target_transformer_name = self.config.target_transformer,
            drop_correlated_threshold = self.config.drop_correlated_threshold,
            feature_selector_threshold = self.config.feature_selector_threshold,
            model_hyperparams = self.config.model_hyperparams,
            preprocessed_dfs = preprocessed_dfs
        )
        logger.info("Model training completed")

        logger.info("Connecting to S3") 
        s3_client = boto3.client('s3')

        logger.info("Fetching model pipeline from S3 bucket")
        try:
            response = s3_client.get_object(
                Bucket=self.config.bucket_name,
                Key=self.config.model_pipeline_key
            )
            content = response["Body"].read()
            existing_model_pipeline = joblib.load(io.BytesIO(content))
        except s3_client.exceptions.NoSuchKey:
            logger.info("No existing model found in S3. Using newly trained model as best.")
            existing_model_pipeline = None

        logger.info("Comparing model performances")
        best_model_pipeline = give_best_model(
            model_pipeline = model_pipeline,
            existing_model_pipeline = existing_model_pipeline,
            preprocessed_dfs = preprocessed_dfs
        )
        logger.info("Compared model performances")

        logger.info("Pushing best model pipeline to S3 bucket")
        model_pipeline_buffer = io.BytesIO()
        joblib.dump(best_model_pipeline, model_pipeline_buffer)
        s3_client.put_object(
            Bucket = self.config.bucket_name,
            Key = self.config.model_pipeline_key,
            Body = model_pipeline_buffer.getvalue()
        )
        logger.info("Best model pipeline pushed to S3 bucket")
     
        return ModelTrainerArtifact()

# Example usage
if __name__ == "__main__":
   try:
        config = ModelTrainerConfig(params = params)
        model_trainer = ModelTrainer(config)
        preprocessed_dfs = model_trainer.ingest_preprocessed()
        model_trainer_artifact = model_trainer.train_evaluate_and_register(preprocessed_dfs)
        print(model_trainer_artifact)

   except Exception as e:
        custom_exp = CustomException(e,sys)
        logger.error(f"{custom_exp}")