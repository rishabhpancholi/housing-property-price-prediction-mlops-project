import os
import yaml
from dotenv import load_dotenv
from dataclasses import dataclass

# Loading the environment variables
load_dotenv()

# Loading params
with open("params.yaml","r") as f:
    params = yaml.safe_load(f)

# Creating a DataIngestionArtifact class
@dataclass
class DataIngestionArtifact:
    """
    This class stores all the artifact variables for data ingestion imported from constants.

    """
    interim_train_data_key:str = os.getenv("INTERIM_TRAIN_DATA_KEY")
    interim_val_data_key:str = os.getenv("INTERIM_VAL_DATA_KEY")
    interim_test_data_key:str = os.getenv("INTERIM_TEST_DATA_KEY")

# Example usage
if __name__ == "__main__":
    dia = DataIngestionArtifact()
    print(dia)