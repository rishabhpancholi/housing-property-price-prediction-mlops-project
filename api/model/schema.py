import numpy as np
from typing import Annotated,Literal,Union,Optional
from pydantic import BaseModel,Field,model_validator,computed_field

# Input schema for prediction model
class HouseFeatures(BaseModel):
    location: Annotated[str,Field(description="Location of the house",examples=["mumbai","noida","thane"])]
    transaction: Annotated[Literal["Resale","New Property","Other","Rent/Lease"],Field(description="Transaction status of the house")]
    furnishing: Annotated[Literal["Unfurnished","Furnished","Semi-Furnished"],Field(description="Furnishing status of the house")]
    facing: Optional[Annotated[Literal["East","North - East","North","West","South","North - West","South - East","South - West"],Field(default=None,description="Facing direction of the house")]]
    ownership: Optional[Annotated[Literal["Freehold","Leasehold","Co-operative Society","Power Of Attorney"],Field(default=None,description="Ownership status of the house")]]
    parking_cover: Annotated[Literal["Open","Covered","No parking"],Field(description="Parking cover status of the house")]
    carpet_area: Optional[Annotated[float,Field(default=None,description="Carpet area of the house in sqft",gt=0)]]
    super_area: Optional[Annotated[float,Field(default=None,description="Super area of the house in sqft",gt=0)]]
    bathroom: Annotated[int,Field(description="Number of bathrooms in the house",gt=0)]
    balcony: Annotated[int,Field(description="Number of balconies in the house",gt=0)]
    num_bhk: Annotated[int,Field(description="Number of bhk in the house",gt=0)]
    floor_num: Annotated[Union[Literal["Undergroung","Ground"],int],Field(description="Floor number of the house")]
    num_floors: Annotated[int,Field(description="Number of floors in the house building",gt=0)]
    overlooking_garden: Annotated[Literal[0,1],Field(description="Whether the house overlooks a garden or not")]
    overlooking_mainroad: Annotated[Literal[0,1],Field(description="Whether the house overlooks a mainroad or not")]
    overlooking_pool: Annotated[Literal[0,1],Field(description="Whether the house overlooks a pool or not")]
    parking_spots: Annotated[int,Field(description="Number of parking spots in the house",ge=0)]

    # Model validations
    @model_validator(mode="after")
    def validate_model(cls,model):
        if isinstance(model.floor_num,str):
            model.floor_num = 0
        if model.num_floors<model.floor_num:
            model.floor_num = model.num_floors
        return model
    
    # Computed fields
    @computed_field
    @property
    def house_size(self)-> str:
        if self.num_bhk < 3:
            return "small"
        elif self.num_bhk <= 4:
            return "normal"
        else:
            return "big"
        
    @computed_field
    @property
    def bathroom_num(self)-> str:
        if self.bathroom < 3:
            return "low"
        elif self.bathroom < 4:
            return "medium"
        else:
            return "high"

    @computed_field
    @property
    def is_unfurnished(self)-> int:
        if self.furnishing == "Unfurnished":
            return 1
        else:
            return 0
        
    @computed_field
    @property
    def floor_height(self)-> str:
        if self.floor_num < 3:
            return "low"
        elif self.floor_num < 6:
            return "medium"
        else:
            return "high"
        
    @computed_field
    @property
    def building_height(self)-> str:
        if self.num_floors < 5:
            return "short"
        elif self.num_floors < 13:
            return "medium"
        else:
            return "tall"
        
    @computed_field
    @property
    def city_tier(self)-> int:
        if self.location in ["mumbai","gurgaon","new-delhi"]:
            return 1
        else:
            return 0
        
    @computed_field
    @property
    def direction_tier(self)-> int:
        if self.facing in ["North - East","North - West"]:
            return 1
        else:
            return 0
        
    @computed_field
    @property
    def has_parking(self)-> str:
        if self.parking_spots == 0:
            return "no parking"
        elif self.parking_spots == 1:
            return "single"
        else:
            return "multiple"
        
    @computed_field
    @property
    def effective_area(self)-> float:
        if self.carpet_area == None:
            return np.log(self.super_area)
        else:
            return np.log(self.carpet_area)
        
    @computed_field
    @property
    def area_per_room(self)-> float:
        return self.effective_area/self.num_bhk
    
    @computed_field
    @property
    def balcony_per_room(self)-> float:
        return self.balcony/self.num_bhk
    
    @computed_field
    @property
    def bathroom_per_room(self)-> float:
        return self.bathroom/self.num_bhk
    
    @computed_field
    @property
    def missingindicator_ownership(self)-> str:
        if self.ownership == None:
            return "True"
        else:
            return "False"
        
    @computed_field
    @property
    def missingindicator_facing(self)-> str:
        if self.facing == None:
            return "True"
        else:
            return "False"
        
    @computed_field
    @property
    def super_areamissing(self)-> str:
        if self.super_area == None:
            return 1
        else:
            return 0
        
    @computed_field
    @property
    def carpet_areamissing(self)-> str:
        if self.carpet_area == None:
            return 1
        else:
            return 0
    





