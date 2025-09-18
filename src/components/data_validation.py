import sys
import pandas as pd
from src.utils import *
from src.logging import get_logger
from src.exception import CustomException
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

# Configure logger
logger = get_logger('data_validation')

# DataValidation class
class DataValidation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.train_file_path = self.data_ingestion_artifact.train_file_path
            self.test_file_path = self.data_ingestion_artifact.test_file_path
            self.schema = self.data_validation_config.schema
        except Exception as e:
            raise CustomException(e,sys)
        
    def validate_number_of_columns(self,dataframe: pd.DataFrame)->bool:
        try:
            logger.info("Validating number of columns")
            number_of_columns = len(self.schema["columns"])
            logger.info(f"Required number of columns: {number_of_columns}")
            logger.info(f"Actual number of columns: {len(dataframe.columns)}")
            return len(dataframe.columns) == number_of_columns
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            logger.info("Initiating data validation")
            logger.info("Reading train and test files")
            train_df = read_data(self.train_file_path)
            test_df = read_data(self.test_file_path)
            logger.info("Reading train and test files completed")

            status_df = self.validate_number_of_columns(train_df) and self.validate_number_of_columns(test_df)
            if not status_df:
                raise CustomException("Train and Test dataframes does not contain all the columns")
            else:
                logger.info("Train and Test dataframes contains all the columns")
                self.data_validation_config.validated_train_file_path.parent.mkdir(parents=True,exist_ok=True)
                self.data_validation_config.validated_test_file_path.parent.mkdir(parents=True,exist_ok=True)
                train_df.to_csv(self.data_validation_config.validated_train_file_path,index=False,header=True)
                test_df.to_csv(self.data_validation_config.validated_test_file_path,index=False,header=True)
            
            logger.info("Data validation completed")

            data_validation_artifact = DataValidationArtifact(
                validation_status=status_df,
                validated_train_file_path=self.data_validation_config.validated_train_file_path,
                validated_test_file_path=self.data_validation_config.validated_test_file_path
            )

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e,sys)