from pydantic_settings import BaseSettings

# App config class
class AppConfig(BaseSettings):
        aws_access_key_id: str
        aws_secret_access_key: str
        model_pipeline_key: str
        bucket_name: str

        class Config:
                env_file = ".env"
