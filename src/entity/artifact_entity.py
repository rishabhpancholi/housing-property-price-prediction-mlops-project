from dataclasses import dataclass

# DataIngestionArtifact class
@dataclass
class DataIngestionArtifact:
    feature_store_path: str
    train_file_path: str
    test_file_path: str

# DataValidationArtifact class
@dataclass
class DataValidationArtifact:
    validation_status: bool
    validated_train_file_path: str
    validated_test_file_path: str

# DataTransformationArtifact class
@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    preprocessor_file_path: str

# ModelTrainerArtifact class
@dataclass
class ModelTrainerArtifact:
    model_file_path: str
    model_train_rmse: float
    model_test_rmse: float