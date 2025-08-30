import sys
import yaml
from src.entity.config_entity import (
    DataPusherConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from src.components.data_pusher import DataPusher
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.logging.logger import get_logger
from src.exceptions.exception_handler import CustomException


logger = get_logger('training_pipeline')

# Loading params
with open("params.yaml","r") as f:
    params = yaml.safe_load(f)

# Creating a TrainingPipeline class
class TrainingPipeline:
    """
    TrainingPipeline class

    """
    def __init__(self,data_pusher, data_ingestion, data_validation, data_transformation, model_trainer):
        self.data_pusher = data_pusher
        self.data_ingestion = data_ingestion
        self.data_validation = data_validation
        self.data_transformation = data_transformation
        self.model_trainer = model_trainer

    def initiate_training_pipeline(self):
        """
        Method to initiate training pipeline

        """
        logger.info("Initiating training_pipeline")

        logger.info("Initiating data pusher")
        raw_df = self.data_pusher.extract_data()
        cleaned_df = self.data_pusher.transform_data(raw_df)
        self.data_pusher.load_data(cleaned_df)
        logger.info("Data push completed")

        logger.info("Initiating data ingestion")
        interim_dfs = self.data_ingestion.ingest_and_split()
        self.data_ingestion.push_interim_to_s3(interim_dfs)
        logger.info("Data ingestion completed")

        logger.info("Initiating data validation")
        self.data_validation.ingest_interim_data_and_validate()
        logger.info("Data validation completed")

        logger.info("Initiating data transformation")
        preprocessed_dfs = self.data_transformation.ingest_interim_and_transform()
        self.data_transformation.push_preprocessed_to_s3(preprocessed_dfs)
        logger.info("Data transformation completed")

        logger.info("Initiating model trainer")
        preprocessed_dfs = self.model_trainer.ingest_preprocessed()
        self.model_trainer.train_evaluate_and_register(preprocessed_dfs)
        logger.info("Model trainer completed")

        logger.info("Training pipeline completed")


# Initiating training pipeline run
try:
    training_pipeline = TrainingPipeline(
        DataPusher(DataPusherConfig()),
        DataIngestion(DataIngestionConfig()),
        DataValidation(DataValidationConfig()),
        DataTransformation(DataTransformationConfig()),
        ModelTrainer(ModelTrainerConfig(params = params))
    )

    training_pipeline.initiate_training_pipeline()
except Exception as e:
    custom_exc = CustomException(e,sys)
    logger.error(f"{custom_exc}")
        








