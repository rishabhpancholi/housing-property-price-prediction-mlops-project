import os
import yaml
import pandas as pd
from dotenv import load_dotenv
from dataclasses import dataclass

# Loading the environment variables
load_dotenv()

# Loading params
with open("params.yaml","r") as f:
    params = yaml.safe_load(f)

# Creating an ETLPipelineArtifact class
@dataclass
class ETLPipelineArtifact:
    """
    This class stores all the artifact variables after ETL pipeline completion.

    """
    raw_data_key:str = os.getenv("RAW_DATA_KEY")

# Creating a DataIngestionArtifact class
@dataclass
class DataIngestionArtifact:
    """
    This class stores all the artifact variables after data ingestion completion.

    """
    interim_train_data_key:str = os.getenv("INTERIM_TRAIN_DATA_KEY")
    interim_val_data_key:str = os.getenv("INTERIM_VAL_DATA_KEY")
    interim_test_data_key:str = os.getenv("INTERIM_TEST_DATA_KEY")

# Creating a DataValidationArtifact class
@dataclass
class DataValidationArtifact(DataIngestionArtifact):
    """
    This class stores all the artifact variables after data validation completion.

    """
# Creating a DataTransformationArtifact class
@dataclass
class DataTransformationArtifact:
    """
    This class stores all the artifact variables after data transformation completion.

    """
    preprocessed_train_data_key:str = os.getenv("PREPROCESSED_TRAIN_DATA_KEY")  
    preprocessed_val_data_key:str = os.getenv("PREPROCESSED_VAL_DATA_KEY")
    preprocessed_test_data_key:str = os.getenv("PREPROCESSED_TEST_DATA_KEY")


# Example usage
if __name__ == "__main__":
    etl = ETLPipelineArtifact()
    dia = DataIngestionArtifact()
    dva = DataValidationArtifact()
    dta = DataTransformationArtifact()
    print(etl)
    print(dia)
    print(dva)
    print(dta)