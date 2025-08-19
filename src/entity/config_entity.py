import os
import yaml
from dotenv import load_dotenv
from dataclasses import dataclass

# Loading the environment variables
load_dotenv()

# Loading params
with open("params.yaml","r") as f:
    params = yaml.safe_load(f)

# Creating a DataIngestionConfig class
@dataclass
class DataIngestionConfig:
    """
    This class stores all the config variables for data ingestion imported from constants.

    """
    bucket_name:str = os.getenv("BUCKET_NAME")
    endpoint_url:str = os.getenv("ENDPOINT_URL")
    region_name:str = os.getenv("REGION_NAME")
    raw_data_key:str = os.getenv("RAW_DATA_KEY")
    interim_train_data_key:str = os.getenv("INTERIM_TRAIN_DATA_KEY")
    interim_val_data_key:str = os.getenv("INTERIM_VAL_DATA_KEY")
    interim_test_data_key:str = os.getenv("INTERIM_TEST_DATA_KEY")
    aws_access_key_id:str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key:str = os.getenv("AWS_SECRET_ACCESS_KEY")
    test_ratio:float = params["split"]["TEST_RATIO"]
    val_ratio:float = params["split"]["VAL_RATIO"]
    test_random_state:int = params["split"]["TEST_RANDOM_STATE"]
    val_random_state:int = params["split"]["VAL_RANDOM_STATE"]

# Example usage
if __name__ == "__main__":
    dic = DataIngestionConfig()
    print(dic)