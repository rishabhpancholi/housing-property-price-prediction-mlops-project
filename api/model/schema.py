from typing import Optional,Literal
from pydantic import BaseModel,Field,model_validator
from api.core.enums import LocationEnum,FacingEnum

# Creating a Pydantic model for input data
class InputSchema(BaseModel):
   """
   This class contains the detailed schema for a particular row in the data.

   """
   location:LocationEnum = Field(description = """
   City in which the house is located.
   Please provide the city name in small letters.""", 
   example = "mumbai")
   num_bhk:int = Field(..., ge = 0, description = "Number of bhks in the house")
   transaction:Literal["Resale", "New Property", "Other", "Rent/Lease"] = Field(description = "Type of transaction")
   furnishing:Optional[Literal["Unfurnished", "Furnished", "Semi-Furnished"]] = Field(description = "Furnishing status of the house", default = None)
   carpet_area:Optional[float] = Field(gt = 0, description = "Carpet area of the house in square feet", default = None)
   super_area:Optional[float] = Field(gt = 0, description = "Super area of the house in square feet", default = None)
   bathroom:Optional[int] = Field(gt = 0, description = "Number of bathrooms in the house", default = None)
   balcony:Optional[int] = Field(ge = 0, description = "Number of balconies in the house", default = None)
   floor_num:Optional[int] = Field(ge = 0, description = "Floor number of the house in the building", default = None)
   num_floors:Optional[int] = Field(ge = 0, description = "Number of floors in the building", default = None)

   @model_validator(mode = "after")
   def validate_num_floors(cls, model):
      """
      Method to validate that num_floors is greater than or equal to floor_num

      """
      if model.floor_num is not None and model.num_floors is not None:
        if model.num_floors < model.floor_num:
            raise ValueError("Number of floors must be greater than or equal to floor number")
      return model
   
   facing:Optional[FacingEnum] = Field(description = "Facing direction of the house", default = None)
   overlooking_garden:Optional[Literal[0,1]] = Field(description = "Whether the house overlooks a garden", default = None)
   overlooking_mainroad:Optional[Literal[0,1]] = Field(description = "Whether the house overlooks the main road", default = None)
   overlooking_pool:Optional[Literal[0,1]] = Field(description = "Whether the house overlooks a pool", default = None)
   ownership:Optional[Literal["Freehold", "Leasehold", "Co-operative Society", "Power Of Attorney"]] = Field(description = "Ownership status of the house", default = None)
   parking_cover:Optional[Literal["Open", "Covered"]] = Field(description = "Whether the house has open or covered parking", default = None)
   parking_spots:Optional[int] = Field(description = "Number of parking spots in the house", default = None)

   @model_validator(mode = "after")
   def validate_string_inputs(cls, model):
      """
      Method to validate that all string inputs are in appropriate casing and no leading or trailing spaces

      """
      model.location = model.location.strip().lower()
      model.transaction = model.transaction.strip().title()
      model.furnishing = model.furnishing.strip().title() if model.furnishing is not None else None
      model.facing = model.facing.strip().title() if model.facing is not None else None
      if model.facing == "South - West":
        model.facing = "South -West"
      model.ownership = model.ownership.strip().title() if model.ownership is not None else None
      model.parking_cover = model.parking_cover.strip().title() if model.parking_cover is not None else None

      return model
