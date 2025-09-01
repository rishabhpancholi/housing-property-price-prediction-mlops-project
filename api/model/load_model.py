import io
import boto3
import joblib
from sklearn.pipeline import Pipeline
from api.core.config import AppConfig

# App Config
config = AppConfig()

# Function to load the model from S3 bucket
def load_model(config: AppConfig)-> Pipeline:
    """
    Loads the model pipeline from S3 bucket

    """
    s3_client = boto3.client("s3")

    response = s3_client.get_object(
        bucket = config.bucket_name,
        key = config.model_pipeline_key
    )

    content = response["Body"].read()
    model_pipeline = joblib.load(io.BytesIO(content))

    return model_pipeline