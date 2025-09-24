import io
import sys
import boto3
import joblib
from src.logging import get_logger
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.entity.config_entity import ModelPusherConfig
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact

# Configure logger
logger = get_logger('model_saver')

# ModelSaver class
class ModelPusher:
    def __init__(self,data_transformation_artifact: DataTransformationArtifact,model_trainer_artifact: ModelTrainerArtifact,model_pusher_config: ModelPusherConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact
        self.model_pusher_config = model_pusher_config

    def push_model_pipeline(self,model_pipeline,key,bucket_name):
        try:
            s3 = boto3.client("s3")
            model_pipeline_buffer = io.BytesIO()
            joblib.dump(model_pipeline,model_pipeline_buffer)
            s3.put_object(
                Bucket = bucket_name,
                Key = key,
                Body = model_pipeline_buffer.getvalue(),
            )
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_model_pusher(self):
        try:
            logger.info("Initiating model pusher")
            preprocessor_file_path = self.data_transformation_artifact.preprocessor_file_path
            model_file_path = self.model_trainer_artifact.model_file_path
            
            logger.info("Reading preprocessor and model files")
            preprocessor = joblib.load(preprocessor_file_path)
            model = joblib.load(model_file_path)
            logger.info("Read preprocessor and model files")

            logger.info("Creating a model pipeline")
            model_pipeline = Pipeline(
                steps = [
                    ("preprocessor",preprocessor),
                    ("model",model)
                ]
            )
            logger.info("Created a model pipeline")

            logger.info("Pushing the model pipeline on S3")
            self.push_model_pipeline(model_pipeline,self.model_pusher_config.model_pipeline_key,self.model_pusher_config.bucket_name)
            logger.info("Pushed the model pipeline on S3")

            logger.info("Model pusher completed")

        except Exception as e:
            raise CustomException(e,sys)
