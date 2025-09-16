from pathlib import Path
from src.constants import *
from src.utils import read_yaml_file

# TrainingPipelineConfig class
class TrainingPipelineConfig:
    def __init__(self):
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_path: Path = Path(ARTIFACT_DIR)
        self.params: dict = read_yaml_file(file_path=Path(PARAMS_FILE_NAME))
        self.schema: dict = read_yaml_file(file_path=Path(SCHEMA_FILE_PATH))


# DataIngestionConfig class
class DataIngestionConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: Path = training_pipeline_config.artifact_path/DATA_INGESTION_DIR_NAME
        self.feature_store_path: Path = self.data_ingestion_dir/DATA_INGESTION_FEATURE_STORE_DIR/FILE_NAME
        self.training_file_path: Path = self.data_ingestion_dir/DATA_INGESTION_INGESTED_DIR/TRAIN_FILE_NAME
        self.testing_file_path: Path = self.data_ingestion_dir/DATA_INGESTION_INGESTED_DIR/TEST_FILE_NAME
        self.bucket_name: str = DATA_INGESTION_BUCKET_NAME
        self.data_key: str = DATA_INGESTION_DATA_KEY
        self.train_test_split_ratio: float = training_pipeline_config.params['data_ingestion']['DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO'] 

# DataValidationConfig class
class DataValidationConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        self.schema: dict = training_pipeline_config.schema
        self.data_validation_dir: Path = training_pipeline_config.artifact_path/DATA_VALIDATION_DIR_NAME
        self.validated_data_dir: Path = self.data_validation_dir/DATA_VALIDATION_VALID_DIR
        self.validated_train_file_path: Path = self.validated_data_dir/TRAIN_FILE_NAME
        self.validated_test_file_path: Path = self.validated_data_dir/TEST_FILE_NAME

# DataTransformationConfig class
class DataTransformationConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir: Path = training_pipeline_config.artifact_path/DATA_TRANSFORMATION_DIR_NAME
        self.transformed_data_dir: Path = self.data_transformation_dir/DATA_TRANSFORMATION_TRANSFORMED_DIR
        self.transformed_train_file_path: Path = self.transformed_data_dir/TRAIN_FILE_NAME
        self.transformed_test_file_path: Path = self.transformed_data_dir/TEST_FILE_NAME
        self.target_column: str = TARGET_COLUMN
        self.preprocessing_object_file_path: Path = self.data_transformation_dir/DATA_TRANSFORMATION_PREPROCESSOR_DIR/DATA_TRANSFORMATION_PREPROCESSOR_FILE_NAME