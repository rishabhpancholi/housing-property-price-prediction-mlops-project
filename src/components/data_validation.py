import io
import sys
import boto3
import numpy as np
import pandas as pd
from pydantic import BaseModel,Field,model_validator
from typing import Optional,Literal

from src.logging.logger import get_logger
from src.exceptions.exception_handler import CustomException
from src.utils.enum_utils import LocationEnum,FacingEnum
from src.entity.config_entity import DataValidationConfig    
from src.entity.artifact_entity import DataValidationArtifact

logger = get_logger('data_validation')

#Creating a HousePriceData class
class HousePriceData(BaseModel):
   """
   This class contains the detailed schema for a particular row in the data.

   """
   location:LocationEnum
   num_bhk:int = Field(..., ge = 0)
   transaction:Literal["Resale", "New Property", "Other", "Rent/Lease"]
   furnishing:Optional[Literal["Unfurnished", "Furnished", "Semi-Furnished"]] = None
   carpet_area:Optional[float] = Field(gt = 0, default = None)
   super_area:Optional[float] = Field(gt = 0, default = None)
   bathroom:Optional[int] = Field(gt = 0, default = None)
   balcony:Optional[int] = Field(ge = 0, default = None)
   floor_num:Optional[int] = Field(ge = 0, default = None)
   num_floors:Optional[int] = Field(ge = 0, default = None)

   @model_validator(mode = "after")
   def validate_num_floors(cls, model):
      if model.floor_num is not None and model.num_floors is not None:
        if model.num_floors < model.floor_num:
            raise ValueError("Number of floors must be greater than or equal to floor number")
      return model
   
   facing:Optional[FacingEnum] = None
   overlooking_garden:Optional[Literal[0,1]] = None
   overlooking_mainroad:Optional[Literal[0,1]] = None
   overlooking_pool:Optional[Literal[0,1]] = None
   ownership:Optional[Literal["Freehold", "Leasehold", "Co-operative Society", "Power Of Attorney"]] = None
   parking_cover:Optional[Literal["Open", "Covered"]] = None
   parking_spots:Optional[int] = None
   amount:float = Field(..., gt = 0)

# Creating a DataValidation class
class DataValidation:
   def __init__(self, config:DataValidationConfig):
      """
      DataValidation class takes DataValidationConfig as input

      """
      self.config = config

   def ingest_interim_data_and_validate(self)-> DataValidationArtifact:
      """
      Method to ingest interim data from S3 bucket and validate

      """
      logger.info("Connecting to S3") 
      s3_client = boto3.client('s3')

      logger.info("Ingesting train, val and test df from S3 bucket")
      interim_dfs = []
      for key in [
         self.config.interim_train_data_key,
         self.config.interim_val_data_key,
         self.config.interim_test_data_key
      ]:
         response = s3_client.get_object(
            Bucket = self.config.bucket_name,
            Key = key
         )

         content = response["Body"].read()
         df = pd.read_csv(io.StringIO(content.decode("utf-8")))
         interim_dfs.append(df)

      logger.info("Converted train,val and test to pandas dataframes")

      logger.info("Validating train,val and test dataframes")
      for df in interim_dfs:
         df = df.replace({np.nan:None})
         columns = df.columns.to_list()
         for _,row in df.iterrows():
            row_pydantic = HousePriceData(**row.to_dict())
            for key in row.to_dict().keys():
               if key not in columns:
                  logger.error(f"Column {key} not found in dataframe")
         
      logger.info("Validation successful")

      return DataValidationArtifact()
          
# Example usage
if __name__ == "__main__":
   try:
        config = DataValidationConfig()
        data_vaildation = DataValidation(config)
        data_validation_artifact = data_vaildation.ingest_interim_data_and_validate()
        print(data_validation_artifact)
   except Exception as e:
        custom_exp = CustomException(e,sys)
        logger.error(f"{custom_exp}")