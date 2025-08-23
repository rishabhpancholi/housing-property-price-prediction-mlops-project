import os
import yaml
from dotenv import load_dotenv
from dataclasses import dataclass

# Loading the environment variables
load_dotenv()

# Loading params
with open("params.yaml","r") as f:
    params = yaml.safe_load(f)

# Creating an ETLPipelineConfig class
@dataclass
class ETLPipelineConfig:
    """
    This class stores config variables required for the ETL pipeline.
    
    """
    bucket_name:str = os.getenv("BUCKET_NAME")
    raw_data_path:str = os.getenv("RAW_DATA_PATH")
    raw_data_key:str = os.getenv("RAW_DATA_KEY")

# Creating a DataIngestionConfig class
@dataclass
class DataIngestionConfig:
    """
    This class stores all the config variables required for data ingestion.

    """
    bucket_name:str = os.getenv("BUCKET_NAME")
    raw_data_key:str = os.getenv("RAW_DATA_KEY")
    interim_train_data_key:str = os.getenv("INTERIM_TRAIN_DATA_KEY")
    interim_val_data_key:str = os.getenv("INTERIM_VAL_DATA_KEY")
    interim_test_data_key:str = os.getenv("INTERIM_TEST_DATA_KEY")
    test_ratio:float = params["split"]["TEST_RATIO"]
    val_ratio:float = params["split"]["VAL_RATIO"]
    test_random_state:int = params["split"]["TEST_RANDOM_STATE"]
    val_random_state:int = params["split"]["VAL_RANDOM_STATE"]

#Creating a DataValidationConfig class
@dataclass
class DataValidationConfig:
    """
    This class stores all the config variables required for data validation.

    """
    bucket_name:str = os.getenv("BUCKET_NAME")
    interim_train_data_key:str = os.getenv("INTERIM_TRAIN_DATA_KEY")
    interim_val_data_key:str = os.getenv("INTERIM_VAL_DATA_KEY")
    interim_test_data_key:str = os.getenv("INTERIM_TEST_DATA_KEY")

#Creating a DataTransformationConfig class
@dataclass
class DataTransformationConfig(DataValidationConfig):
    """
    This class stores all the config variables required for data transformation.

    """
    


# Example usage
if __name__ == "__main__":
    etl = ETLPipelineConfig()
    print(etl)
    dic = DataIngestionConfig()
    print(dic)
    dvc = DataValidationConfig()
    print(dvc)
    dtc = DataTransformationConfig()
    print(dtc)