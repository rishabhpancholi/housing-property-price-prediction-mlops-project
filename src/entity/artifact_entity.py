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

# Creating a DataPusherArtifact class
@dataclass
class DataPusherArtifact:
    """
    This class stores all the artifact variables after data pusher completion.

    """
    raw_data_key:str = os.getenv("RAW_DATA_KEY")

# Creating a DataIngestionArtifact class
@dataclass
class DataIngestionArtifact:
    """
    This class stores all the artifact variables after data ingestion completion.

    """
    interim_train_data_key:str = os.getenv("INTERIM_TRAIN_DATA_KEY")
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
    preprocessed_test_data_key:str = os.getenv("PREPROCESSED_TEST_DATA_KEY")

@dataclass
class ModelTrainerArtifact:
    """
    This class stores all the artifact variables after model training completion.

    """
    model_pipeline_key:str = os.getenv("MODEL_PIPELINE_KEY")


# Example usage
if __name__ == "__main__":
    dpa = DataPusherArtifact()
    dia = DataIngestionArtifact()
    dva = DataValidationArtifact()
    dta = DataTransformationArtifact()
    mta = ModelTrainerArtifact()
    print(dpa)
    print(dia)
    print(dva)
    print(dta)
    print(mta)