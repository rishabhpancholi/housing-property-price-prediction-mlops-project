import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

"""Common constants for training pipeline"""
TARGET_COLUMN: str = "amount"
PIPELINE_NAME: str = "housing_price_pipeline"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "houses.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
PARAMS_FILE_NAME: str = "params.yaml"
SCHEMA_FILE_PATH: str = "data_schema/schema.yaml"

"""Data Ingestion related constants"""
DATA_INGESTION_BUCKET_NAME: str = "housepricesbucket130256"
DATA_INGESTION_DATA_KEY: str = "data/houses.csv"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"


"""Data Validation related constants"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"

"""Data Transformation related constants"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR: str = "transformed"
DATA_TRANSFORMATION_PREPROCESSOR_DIR: str = "preprocessor"
DATA_TRANSFORMATION_PREPROCESSOR_FILE_NAME: str = "preprocessor.joblib"

"""Model Trainer related constants"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR_NAME: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME: str = "model.joblib"

"""Model Pusher related constants"""
MODEL_PUSHER_BUCKET_NAME: str = "housepricesbucket130256"
MODEL_PUSHER_MODEL_PIPELINE_KEY: str = "model_pipeline"
