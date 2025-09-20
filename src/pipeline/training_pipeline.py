import sys
from src.logging import get_logger
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact

# Configure logger
logger = get_logger('training_pipeline')

# TrainingPipeline class
class TrainingPipeline:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        self.training_pipeline_config = training_pipeline_config
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        self.data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        self.data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline_config)

    def start_data_ingestion(self)->DataIngestionArtifact:
        self.data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
        self.data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()
        return self.data_ingestion_artifact
    
    def start_data_validation(self)->DataValidationArtifact:
        self.data_validation = DataValidation(data_ingestion_artifact=self.data_ingestion_artifact,data_validation_config=self.data_validation_config)
        self.data_validation_artifact = self.data_validation.initiate_data_validation()
        return self.data_validation_artifact
    
    def start_data_transformation(self)->DataTransformationArtifact:
        self.data_transformation = DataTransformation(data_validation_artifact=self.data_validation_artifact,data_transformation_config=self.data_transformation_config)
        self.data_transformation_artifact = self.data_transformation.initiate_data_transformation()
        return self.data_transformation_artifact
    
    def start_model_trainer(self)->ModelTrainerArtifact:
        self.model_trainer = ModelTrainer(data_transformation_artifact=self.data_transformation_artifact,model_trainer_config=self.model_trainer_config)
        self.model_trainer_artifact = self.model_trainer.initiate_model_trainer()
        return self.model_trainer_artifact
    
if __name__ == "__main__":
    try:
        logger.info("Initiating training pipeline")
        training_pipeline_config = TrainingPipelineConfig()
        training_pipeline = TrainingPipeline(training_pipeline_config=training_pipeline_config)

        data_ingestion_artifact = training_pipeline.start_data_ingestion()
        data_validation_artifact = training_pipeline.start_data_validation()
        data_transformation_artifact = training_pipeline.start_data_transformation()
        model_trainer_artifact = training_pipeline.start_model_trainer()

        logger.info(f"Training pipeline completed with train mae {model_trainer_artifact.model_train_mae} and test mae {model_trainer_artifact.model_test_mae}")
    except Exception as e:
        raise CustomException(e,sys)