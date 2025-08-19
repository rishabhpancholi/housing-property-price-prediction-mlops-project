import yaml
from pathlib import Path
from dataclasses import dataclass

# Loading params
with open("params.yaml","r") as f:
    params = yaml.safe_load(f)

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Creating a DataIngestionArtifact class
@dataclass
class DataIngestionArtifact:
    """
    This class stores all the artifact variables for data ingestion imported from constants.

    """
    train_data_path:Path = BASE_DIR/Path(params["interim_data_paths"]["TRAIN_DATA_PATH"])
    val_data_path:Path = BASE_DIR/Path(params["interim_data_paths"]["VAL_DATA_PATH"])
    test_data_path:Path = BASE_DIR/Path(params["interim_data_paths"]["TEST_DATA_PATH"])

# Example usage
if __name__ == "__main__":
    dia = DataIngestionArtifact()
    print(dia)