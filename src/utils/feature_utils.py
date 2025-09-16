import numpy as np
import pandas as pd

# Function to make features in train and test dataframes
def make_features(df: pd.DataFrame)->pd.DataFrame:

   # Function to bin house sizes
   def house_size_binner(X):

      return (
            X.assign(
                house_size = lambda df: (
                    np.select(
                    [
                        df.num_bhk.between(1,3,inclusive = "left"),
                        df.num_bhk.between(3,4,inclusive = "left")
                    ],
                    ["small","normal"],
                    default = "big"
                )
                ) 
            )
        )
   
   df = house_size_binner(df)
   
   # Function to bin bathroom number
   def bathroom_num_binner(X):

    return (
        X.assign(
               bathroom_num = lambda df: (
                np.select(
                [
                    df.bathroom.between(1,3,inclusive = "left"),
                    df.bathroom.between(3,4,inclusive = "left")
                ],
                ["low","medium"],
                default = "high"
              )
            ) 
        )
    )
   
   df = bathroom_num_binner(df)

   # Function to check is unfurnished
   def is_unfurnished(X):


    return (
        X.assign(
            is_unfurnished = lambda df:(
                    np.where(
                      df.furnishing.eq('Unfurnished'),1,0
                    )
            )
        )
    )
   
   df = is_unfurnished(df)
   
   # Function to bin floor height
   def floor_height_binner(X):


    return (
        X.assign(
            floor_height = lambda df:(
                    np.select(
                        [
                            (df.floor_num.between(0,3, inclusive = "left")),
                            (df.floor_num.between(3,6, inclusive = "left"))
                        ],
                        ["low","medium"],
                        default = "high"
                    )
            )
        )
    )
   
   df = floor_height_binner(df)
   
   # Function to bin building height
   def building_height_binner(X):


    return (
        X.assign(
            building_height = lambda df:(
                np.select(
                [
                    (df.num_floors.between(0,5, inclusive = "left")),
                    (df.num_floors.between(5,13, inclusive = "left"))
                ],
                ["short","medium"],
                default = "tall"
            )
            )
        )
    )
   
   df = building_height_binner(df)
   
   # Function to bin cities
   def city_binner(X):
    


     return (
        X.assign(
            city_tier = lambda df:(
                np.where(
                    df.location.isin(["mumbai","gurgaon","new-delhi"]),
                    1,
                    0
                )
            )
        )
    )
   
   df = city_binner(df)
   
   # Function to round balcony to nearest integer
   def nearest_integer(X):


     return (
        X.assign(
            balcony = lambda df:(
                np.round(df.balcony)
            )
        )
     )
   
   df = nearest_integer(df)
   
   # Function to bin direction
   def direction_binner(X):



     return (
        X.assign(
            direction_tier = lambda df:(
                np.where(
                    df.facing.isin(["North - East","North - West"]),
                    1,
                    0
                )
            )
        )
     )
   
   df = direction_binner(df)
   
   # Function to check has parking
   def has_parking(X):


    return (
        X.assign(
            has_parking = lambda df:(
                np.select(
                            [
                                df.parking_spots.eq(0),
                                df.parking_spots.eq(1)
                            ],
                            ["no parking","single"],
                            default = "multiple"
                        )
            )
        )
     )
   
   df = has_parking(df)
   
   # Function to check effective area
   def effective_area(X):


    return(
        X
        .assign(
            effective_area = lambda df:(
                np.where(
                    df.carpet_area.eq(-1),
                    df.super_area,
                    df.carpet_area
                )
            ),
            carpet_areamissing = lambda df:(
                np.where(
                    df.carpet_area.eq(-1),
                    1,
                    0
                )
            ),
            super_areamissing = lambda df:(
                np.where(
                    df.super_area.eq(-1),
                    1,
                    0
                )
            )
        )
    )
   
   df = effective_area(df)

   # Function to log transform effective area
   def effective_area_log(X):


     return(
            X
            .assign(
                effective_area = lambda df:(
                    np.log(df.effective_area)
                )
            )
        )
   
   df = effective_area_log(df)
   
   # Function for area per room
   def area_per_room(X):


    return(
        X
        .assign(
            area_per_room = lambda df:(
                np.where(
                    df.carpet_area.eq(-1),
                    df.super_area/df.num_bhk,
                    df.carpet_area/df.num_bhk
                )
            )
        )
    )
   
   df = area_per_room(df)
   
   # Function for balcony per room
   def balcony_per_room(X):


    return(
        X
        .assign(
            balcony_per_room = lambda df:(
                df.balcony/df.num_bhk
            )
        )
    )
   
   df = balcony_per_room(df)
   
   # Function for bathroom per room
   def bathroom_per_room(X):

    return(
        X
        .assign(
            bathroom_per_room = lambda df:(
                df.bathroom/df.num_bhk
            )
        )
    )
   
   df = bathroom_per_room(df)

   return df
    
    