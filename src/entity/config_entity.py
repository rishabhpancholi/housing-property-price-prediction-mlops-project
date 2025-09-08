import yaml
from pathlib import Path
from src.constants import *
from datetime import datetime

# Loading Params
params = yaml.safe_load(open('params.yaml'))

# TrainingPipelineConfig class
class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        timestamp: str = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_path: Path = Path(ARTIFACT_DIR)/timestamp


# DataIngestionConfig class
class DataIngestionConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: Path = training_pipeline_config.artifact_path/DATA_INGESTION_DIR_NAME
        self.feature_store_path: Path = self.data_ingestion_dir/DATA_INGESTION_FEATURE_STORE_DIR/FILE_NAME
        self.training_file_path: Path = self.data_ingestion_dir/DATA_INGESTION_INGESTED_DIR/TRAIN_FILE_NAME
        self.testing_file_path: Path = self.data_ingestion_dir/DATA_INGESTION_INGESTED_DIR/TEST_FILE_NAME
        self.mongo_db_url: str = DATA_INGESTION_MONGO_DB_URL
        self.collection_name: str = DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = DATA_INGESTION_DATABASE_NAME
        self.train_test_split_ratio: float = params['data ingestion']['DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO'] 
