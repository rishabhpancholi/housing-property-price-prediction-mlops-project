import sklearn
import numpy as np
import pandas as pd
from typing import Tuple
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline,FeatureUnion
from feature_engine.encoding import RareLabelEncoder
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder,TargetEncoder,RobustScaler,MinMaxScaler,FunctionTransformer

#Setting output to pandas dataframes
sklearn.set_config(transform_output = 'pandas')

# Function to transform data
def transform_data(interim_dfs: Tuple[pd.DataFrame, pd.DataFrame])-> Tuple[pd.DataFrame, pd.DataFrame]:

    """
    Method to preprocess train and test dataframes

    """

    # Column Transformers
    transaction_transformer = Pipeline(steps = [
        ("grouper",RareLabelEncoder(tol = 0.1, n_categories = 2, replace_with = "Resale")),
        ("encoder",OneHotEncoder(sparse_output = False,handle_unknown = 'ignore'))
    ])

    def house_size_binner(X):
        columns = X.columns.to_list()

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
            .drop(columns = columns)
        )

    num_bhk_pipe1 = Pipeline(steps = [
        ("scaler",MinMaxScaler())
    ])

    num_bhk_pipe2 = Pipeline(steps = [
        ("house_size_binner",FunctionTransformer(func = house_size_binner)),
        ("encoder",OrdinalEncoder(categories = [["small","normal","big"]]))
    ])

    num_bhk_transformer = FeatureUnion(transformer_list = [
        ("num_bhk_pipe1",num_bhk_pipe1),
        ("num_bhk_pipe2",num_bhk_pipe2)
    ])

    def bathroom_num_binner(X):
        columns = X.columns.to_list()

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
            .drop(columns = columns)
        )

    bathroom_pipe1 = Pipeline(steps = [
        ("scaler",MinMaxScaler())
    ])

    bathroom_pipe2 = Pipeline(steps = [
        ("bathroom_num_binner",FunctionTransformer(func = bathroom_num_binner)),
        ("encoder",OrdinalEncoder(categories = [["low","medium","high"]]))
    ])

    bathroom_transformer = FeatureUnion(transformer_list = [
        ("bathroom_pipe1",bathroom_pipe1),
        ("bathroom_pipe2",bathroom_pipe2)
    ])

    def bathroom_num_binner(X):
        columns = X.columns.to_list()

    furnishing_pipe1 = Pipeline(steps = [
        ("encoder",OrdinalEncoder(categories = [["Unfurnished","Semi-Furnished","Furnished"]])),
    ])

    furnishing_pipe2 = Pipeline(steps = [
        ("is_unfurnished",FunctionTransformer(func = lambda x: np.where(x == 'Unfurnished',1,0)))
    ])

    furnishing_transformer = FeatureUnion(transformer_list = [
        ("furnishing_pipe1",furnishing_pipe1),
        ("furnishing_pipe2",furnishing_pipe2)
    ])

    def floor_height_binner(X):

        columns = X.columns.to_list()

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
            .drop(columns = columns)
        )

    def building_height_binner(X):

        columns = X.columns.to_list()

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
            .drop(columns = columns)
        )

    floor_num_pipe1 = Pipeline(steps = [
        ("scaler",RobustScaler())
    ])

    floor_num_pipe2 = Pipeline(steps = [
        ("floor_height_binner",FunctionTransformer(func = floor_height_binner)),
        ("encoder",OrdinalEncoder(categories = [["low","medium","high"]])),
    ])

    floor_num_transformer = FeatureUnion(transformer_list = [
        ("floor_num_pipe1",floor_num_pipe1),
        ("floor_num_pipe2",floor_num_pipe2)
    ])

    num_floors_pipe1 = Pipeline(steps = [
        ("scaler",RobustScaler())
    ])

    num_floors_pipe2 = Pipeline(steps = [
        ("building_height_binner",FunctionTransformer(func = building_height_binner)),
        ("encoder",OrdinalEncoder(categories = [["short","medium","tall"]]))
    ])

    num_floors_transformer = FeatureUnion(transformer_list = [
        ("num_floors_pipe1",num_floors_pipe1),
        ("num_floors_pipe2",num_floors_pipe2)
    ])

    def city_binner(X):
        
        columns = X.columns.to_list()

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
            .drop(columns = columns)
        )

    location_pipe1 = Pipeline(steps = [
        ("target_encoder", TargetEncoder())
    ])

    location_pipe2 = Pipeline(steps = [
        ("city_binner",FunctionTransformer(func = city_binner))
    ])

    location_transformer = FeatureUnion(transformer_list = [
        ("location_pipe1",location_pipe1),
        ("location_pipe2",location_pipe2)
    ])

    def price_binner(X):

        columns = X.columns.to_list()

        return (
            X.assign(
                price_range = lambda df:(
                    np.select(
                        [
                            df.price.between(0,4000,inclusive = "left"),
                            df.price.between(4000,6000,inclusive = "left")
                        ],
                        ["low","medium"],
                        default = "high"
                    )
                )
            )
            .drop(columns = columns)
        )

    balcony_transformer = Pipeline(steps = [
        ("nearest_integer",FunctionTransformer(func = lambda x : np.round(x))),
        ("scaler",MinMaxScaler())
    ])

    ownership_transformer = Pipeline(steps = [
        ("encoder",OneHotEncoder(sparse_output = False,handle_unknown = 'ignore'))
    ])

    missingindicator_ownership_transformer = Pipeline(steps = [
        ("encoder",OneHotEncoder(drop = 'first',sparse_output = False,handle_unknown = 'ignore'))
    ])

    def direction_binner(X):

        columns = X.columns.to_list()

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
            .drop(columns = columns)
        )

    facing_pipe1 = Pipeline(steps = [
        ("encoder",OneHotEncoder(sparse_output = False,handle_unknown = 'ignore'))
    ])

    facing_pipe2 = Pipeline(steps = [
        ("direction_binner",FunctionTransformer(func = direction_binner))
    ])

    facing_pipe3 = Pipeline(steps = [
        ("target_encoder",TargetEncoder())
    ])

    facing_transformer = FeatureUnion(transformer_list = [
        ("facing_pipe1",facing_pipe1),
        ("facing_pipe2",facing_pipe2),
        ("facing_pipe3",facing_pipe3)
    ])

    missingindicator_facing_transformer = Pipeline(steps = [
        ("encoder",OneHotEncoder(drop = 'first',sparse_output = False,handle_unknown = 'ignore'))
    ])

    overlooking_garden_transformer = Pipeline(steps = [
        ("encoder",OneHotEncoder(sparse_output = False,handle_unknown = 'ignore'))
    ])

    overlooking_mainroad_transformer = Pipeline(steps = [
        ("encoder",OneHotEncoder(categories=[[ -1, 0, 1 ]], drop=[-1], sparse_output=False, handle_unknown='ignore'))
    ])

    overlooking_pool_transformer = Pipeline(steps = [
        ("encoder",OneHotEncoder(categories=[[ -1, 0, 1 ]], drop=[-1], sparse_output=False, handle_unknown='ignore'))
    ])

    parking_cover_transformer = Pipeline(steps = [
        ("encoder",OneHotEncoder(sparse_output = False,handle_unknown = 'ignore'))
    ])

    def has_parking(X):

        columns = X.columns.to_list()

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
            .drop(columns = columns)
        )

    parking_spots_transformer = Pipeline(steps = [
        ("has_parking",FunctionTransformer(func = has_parking)),
        ("encoder",OneHotEncoder(categories = [["multiple","single","no parking"]],drop = [["no parking"]],sparse_output = False,handle_unknown = 'ignore'))
    ])

    def effective_area(X):

        columns = X.columns.to_list()

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
            .drop(columns = columns)
        )

    scaler_pipeline = Pipeline(steps = [
        ("log_transformer",FunctionTransformer(func = lambda x: np.log(x))),
        ("scaler",RobustScaler())
    ])

    area_transformer = Pipeline(steps = [
        ("effective_area",FunctionTransformer(func = effective_area)),
        ("scaler_pipeline",ColumnTransformer(transformers = [
            ("scaler_pipeline",scaler_pipeline,["effective_area"])
        ],remainder = "passthrough")),
    ])

    def area_per_room(X):

        columns = X.columns.to_list()

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
            .drop(columns = columns)
        )


    area_per_room_transformer = Pipeline(steps = [
        ("area_per_room",FunctionTransformer(func = area_per_room)),
        ("scaler_pipeline",ColumnTransformer(transformers = [
            ("scaler_pipeline",scaler_pipeline,["area_per_room"])
        ],remainder = "passthrough"))
    ])

    def balcony_per_room(X):

        columns = X.columns.to_list()

        return(
            X
            .assign(
                balcony_per_room = lambda df:(
                    df.balcony/df.num_bhk
                )
            )
            .drop(columns = columns)
        )

    def bathroom_per_room(X):

        columns = X.columns.to_list()

        return(
            X
            .assign(
                bathroom_per_room = lambda df:(
                    df.bathroom/df.num_bhk
                )
            )
            .drop(columns = columns)
        )

    balcony_per_room_transformer = Pipeline(steps = [
        ("balcony_per_room",FunctionTransformer(func = balcony_per_room))
    ])

    bathroom_per_room_transformer = Pipeline(steps = [
        ("bathroom_per_room",FunctionTransformer(func = bathroom_per_room))
    ])

    column_transformer = ColumnTransformer(transformers = [
        ("transaction_transformer",transaction_transformer,["transaction"]),
        ("num_bhk_transformer",num_bhk_transformer,["num_bhk"]),
        ("bathroom_transformer",bathroom_transformer,["bathroom"]),
        ("furnishing_transformer",furnishing_transformer,["furnishing"]),
        ("floor_num_transformer",floor_num_transformer,["floor_num"]),
        ("num_floors_transformer",num_floors_transformer,["num_floors"]),
        ("location_transformer",location_transformer,["location"]),
        ("balcony_transformer",balcony_transformer,["balcony"]),
        ("ownership_transformer",ownership_transformer,["ownership"]),
        ("missingindicator_ownership_transformer",missingindicator_ownership_transformer,["missingindicator_ownership"]),
        ("facing_transformer",facing_transformer,["facing"]),
        ("missingindicator_facing_transformer",missingindicator_ownership_transformer,["missingindicator_facing"]),
        ("overlooking_garden_transformer",overlooking_garden_transformer,["overlooking_garden"]),
        ("overlooking_mainroad_transformer",overlooking_mainroad_transformer,["overlooking_mainroad"]),
        ("overlooking_pool_transformer",overlooking_pool_transformer,["overlooking_pool"]),
        ("parking_cover_transformer",parking_cover_transformer,["parking_cover"]),
        ("parking_spots_transformer",parking_spots_transformer,["parking_spots"]),
        ("area_transformer",area_transformer,["carpet_area","super_area"]),
        ("area_per_room_transformer",area_per_room_transformer,["carpet_area","super_area","num_bhk"]),
        ("balcony_per_room_transformer",balcony_per_room_transformer,["balcony","num_bhk"]),
        ("bathroom_per_room_transformer",bathroom_per_room_transformer,["bathroom","num_bhk"])
    ],remainder = 'passthrough')
        
    train_df, test_df = interim_dfs

    transformed_train_df = column_transformer.fit_transform(train_df, train_df['amount'])
    transformed_test_df = column_transformer.transform(test_df)

    return (transformed_train_df, transformed_test_df)



