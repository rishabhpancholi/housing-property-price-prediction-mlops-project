import io
import boto3
import joblib
from api.config import AppConfig
from sklearn.pipeline import Pipeline
from botocore.client import BaseClient

# Setting up app config
app_config = AppConfig()

# Setting up boto client
client = boto3.client(
    's3',
    aws_access_key_id=app_config.aws_access_key_id,
    aws_secret_access_key=app_config.aws_secret_access_key
)

# Function to load model
def load_model(client: BaseClient = client, app_config: AppConfig = app_config)->Pipeline:
    try:
        response = client.get_object(
            Bucket = app_config.bucket_name,
            Key = app_config.model_pipeline_key
        )

        model_pipeline_buffer = io.BytesIO(response['Body'].read())
        model_pipeline = joblib.load(model_pipeline_buffer)
        return model_pipeline
    except Exception as e:
        raise Exception(f"Failed to laod model from s3: {e}")


