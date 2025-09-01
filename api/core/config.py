import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Loading the environment variables
load_dotenv()

# Creating an AppConfig class
@dataclass
class AppConfig:
    """
    This class stores all the config variables required for the application.
    
    """
    redis_url:str = os.getenv('REDIS_URL')
    bucket_name:str = os.getenv('BUCKET_NAME')
    model_pipeline_key:str = os.getenv('MODEL_PIPELINE_KEY')

# Example usage
if __name__ == "__main__":
  app_config = AppConfig()
  print(app_config)