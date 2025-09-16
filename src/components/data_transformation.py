import sys
import pandas as pd
from pathlib import Path
from sklearn.pipeline import Pipeline

from src.utils import *
from src.logging import get_logger
from src.exception import CustomException
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact

# Configure logger
logger = get_logger('data_transformation')

# DataTransformation class
class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact,data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self.train_file_path = self.data_validation_artifact.validated_train_file_path
            self.test_file_path = self.data_validation_artifact.validated_test_file_path
            self.target_column = self.data_transformation_config.target_column
            self.preprocessor_object_file_path = self.data_transformation_config.preprocessing_object_file_path
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logger.info("Initiating data transformation")
            logger.info("Reading train and test files")
            train_df = read_data(self.train_file_path)
            test_df = read_data(self.test_file_path)
            logger.info("Reading train and test files completed")
            
            X_train = train_df.drop(columns = [self.target_column],axis=1)
            y_train = train_df[self.target_column].copy()
            
            X_test = test_df.drop(columns = [self.target_column],axis=1)
            y_test = test_df[self.target_column].copy()

            logger.info("Imputing missing values in train and test dataframes")
            imputer = get_imputer_object()
            X_train = imputer.fit_transform(X_train)
            X_test = imputer.transform(X_train)
            logger.info("Imputed missing values in train and test dataframes")

            logger.info("Making features in train and test dataframes")
            X_train = make_features(X_train)
            X_test = make_features(X_test)
            logger.info("Made features in train and test dataframes")

            logger.info("Transforming train and test dataframes")
            transformer = get_transformer_object()
            X_train = transformer.fit_transform(X_train,y_train)
            X_test = transformer.transform(X_test)
            logger.info("Transformed train and test dataframes")

            logger.info("Saving transformed train and test dataframes")
            transformed_train_df = X_train.join(y_train)
            transformed_test_df = X_test.join(y_test)
            self.data_transformation_config.transformed_train_file_path.parent.mkdir(parents=True,exist_ok=True)
            self.data_transformation_config.transformed_test_file_path.parent.mkdir(parents=True,exist_ok=True)
            transformed_train_df.to_csv(self.data_transformation_config.transformed_train_file_path,index=False,header=True)
            transformed_test_df.to_csv(self.data_transformation_config.transformed_test_file_path,index=False,header=True)
            logger.info("Saved transformed train and test dataframes")

            logger.info("Saving preprocessor object")
            self.preprocessor_object_file_path.parent.mkdir(parents=True,exist_ok=True)
            save_joblib_file(self.preprocessor_object_file_path,transformer)
            logger.info("Saved preprocessor object")

            logger.info("Data transformation completed")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocessor_file_path=self.preprocessor_object_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
            
