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
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key:str = os.getenv("AWS_SECRET_ACCESS_KEY")
    raw_data_s3_path: str = os.getenv("RAW_DATA_S3_PATH")
    test_ratio: float = params["train_test_split"]["TEST_RATIO"]
    val_ratio: float = params["train_test_split"]["VAL_RATIO"]

# Example usage
if __name__ == "__main__":
    dic = DataIngestionConfig()
    print(dic)