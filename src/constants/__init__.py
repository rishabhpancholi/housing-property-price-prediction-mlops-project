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

"""Data Ingestion related constants"""
DATA_INGESTION_MONGO_DB_URL: str = os.getenv("MONGO_DB_URL")
DATA_INGESTION_DATABASE_NAME: str = "housing-property-price-prediction"
DATA_INGESTION_COLLECTION_NAME: str = "HouseData"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
