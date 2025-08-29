import os
import yaml
from dotenv import load_dotenv
from dataclasses import dataclass,field

# Loading the environment variables
load_dotenv()

# Loading params
with open("params.yaml","r") as f:
    params = yaml.safe_load(f)

# Creating a DataPusherConfig class
@dataclass
class DataPusherConfig:
    """
    This class stores config variables required for the data pusher.
    
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
    interim_test_data_key:str = os.getenv("INTERIM_TEST_DATA_KEY")
    test_size:float = params["split"]["TEST_SIZE"]
    random_state:int = params["split"]["RANDOM_STATE"]

#Creating a DataValidationConfig class
@dataclass
class DataValidationConfig:
    """
    This class stores all the config variables required for data validation.

    """
    bucket_name:str = os.getenv("BUCKET_NAME")
    interim_train_data_key:str = os.getenv("INTERIM_TRAIN_DATA_KEY")
    interim_test_data_key:str = os.getenv("INTERIM_TEST_DATA_KEY")

#Creating a DataTransformationConfig class
@dataclass
class DataTransformationConfig(DataValidationConfig):
    """
    This class stores all the config variables required for data transformation.

    """
    preprocessed_train_data_key:str = os.getenv("PREPROCESSED_TRAIN_DATA_KEY")
    preprocessed_test_data_key:str = os.getenv("PREPROCESSED_TEST_DATA_KEY")

@dataclass
class ModelTrainerConfig:
    """
    This class stores all the config variables required for model training.

    """
    params:dict

    bucket_name:str = os.getenv("BUCKET_NAME")
    preprocessed_train_data_key:str = os.getenv("PREPROCESSED_TRAIN_DATA_KEY")
    preprocessed_test_data_key:str = os.getenv("PREPROCESSED_TEST_DATA_KEY")
    target_transformer:str = params["train"]["TARGET_TRANSFORMER"]
    drop_correlated_threshold:float = params["train"]["DROP_CORRELATED_THRESHOLD"]
    feature_selector_threshold:float = params["train"]["FEATURE_SELECTOR_THRESHOLD"]

    regressor:str = field(init = False)
    model_hyperparams:dict = field(init = False)

    def __post_init__(self):
        """
        Method to dynamically initialize model params based on regressor

        """
        train_cfg = self.params["train"]

        self.regressor = train_cfg["REGRESSOR"]
        self.model_hyperparams = train_cfg.get(self.regressor, {})


# Example usage
if __name__ == "__main__":
    dpc = DataPusherConfig()
    print(dpc)
    dic = DataIngestionConfig()
    print(dic)
    dvc = DataValidationConfig()
    print(dvc)
    dtc = DataTransformationConfig()
    print(dtc)
    mtc = ModelTrainerConfig(params = params)
    print(mtc)