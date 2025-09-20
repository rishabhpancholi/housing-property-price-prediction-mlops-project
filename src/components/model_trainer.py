import sys
import mlflow
import dagshub
import pandas as pd
from src.utils import *
from src.logging import get_logger
from src.exception import CustomException
from sklearn.metrics import mean_absolute_error
from sklearn.compose import TransformedTargetRegressor
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact

# Configure logger
logger = get_logger('model_trainer')

# ModelTrainer class
class ModelTrainer:
    def __init__(self,data_transformation_artifact: DataTransformationArtifact,model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
            self.train_file_path = self.data_transformation_artifact.transformed_train_file_path
            self.test_file_path = self.data_transformation_artifact.transformed_test_file_path
            self.trained_model_path = self.model_trainer_config.trained_model_file_path
            self.target_column = self.model_trainer_config.target_column
        except Exception as e:
            raise CustomException(e,sys)
         
    def evaluate_model(self,trained_model: TransformedTargetRegressor,X_train: pd.DataFrame,y_train: pd.Series,X_test: pd.DataFrame,y_test: pd.Series)->dict:
         try:
              y_train_pred = trained_model.predict(X_train)
              y_test_pred = trained_model.predict(X_test)

              train_mae = mean_absolute_error(y_train,y_train_pred)
              test_mae = mean_absolute_error(y_test,y_test_pred)

              params_dict = {
                   "train_mae": train_mae,
                   "test_mae": test_mae
              }

              return params_dict
         except Exception as e:
              raise CustomException(e,sys)

    
    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            logger.info("Initiating model trainer")
            logger.info("Reading train and test files")
            train_df = read_data(self.train_file_path)
            test_df = read_data(self.test_file_path)
            logger.info("Reading train and test files completed")

            X_train = train_df.drop(columns = [self.target_column],axis=1)
            y_train = train_df[self.target_column].copy()
            
            X_test = test_df.drop(columns = [self.target_column],axis=1)
            y_test = test_df[self.target_column].copy()

            dagshub.init(repo_owner='rishabhpancholi', repo_name='housing-property-price-prediction-mlops-project', mlflow=True)

            with mlflow.start_run():
                logger.info("Tuning the model and finding best params")
                trained_model,best_params = train_model(X_train,y_train,self.model_trainer_config.kfold_nsplits,self.model_trainer_config.optuna_ntrials)
                mlflow.log_params(best_params)
                logger.info("Trained and tuned the model for best params")

                logger.info("Evaluating the model")
                model_metrics = self.evaluate_model(trained_model,X_train,y_train,X_test,y_test)
                mlflow.log_metrics(model_metrics)
                logger.info("Model evaluated")

            logger.info("Saving the model")
            self.trained_model_path.parent.mkdir(parents=True,exist_ok=True)
            save_joblib_file(self.trained_model_path,trained_model)
            logger.info("Saved the model")

            logger.info("Model trainer completed")

            model_trainer_artifact = ModelTrainerArtifact(
                 model_file_path=self.trained_model_path,
                 model_train_mae=model_metrics["train_mae"],
                 model_test_mae=model_metrics["test_mae"]
            )
            return model_trainer_artifact
        except Exception as e:
                raise CustomException(e,sys)