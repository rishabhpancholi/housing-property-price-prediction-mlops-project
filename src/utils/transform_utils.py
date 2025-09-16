import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline,FeatureUnion
from feature_engine.encoding import RareLabelEncoder
from sklearn.preprocessing import OneHotEncoder,MinMaxScaler,RobustScaler,OrdinalEncoder,TargetEncoder

# Setting sklearn config to pandas
sklearn.set_config(transform_output='pandas')

def get_transformer_object()-> ColumnTransformer:

    transaction_transformer = Pipeline(steps = [
        ("grouper",RareLabelEncoder(tol = 0.1, n_categories = 2, replace_with = "Resale")),
        ("encoder",OneHotEncoder(sparse_output = False,handle_unknown = 'ignore'))
    ])

    num_bhk_scaler = MinMaxScaler()

    house_size_encoder = OrdinalEncoder(categories = [["small","normal","big"]])

    bathroom_scaler = MinMaxScaler()

    bathroom_num_encoder = OrdinalEncoder(categories = [["low","medium","high"]])

    furnishing_encoder = OrdinalEncoder(categories = [["Unfurnished","Semi-Furnished","Furnished"]])

    floor_num_scaler = RobustScaler()

    floor_height_encoder = OrdinalEncoder(categories = [["low","medium","high"]])

    num_floors_scaler = RobustScaler()

    building_height_encoder = OrdinalEncoder(categories = [["short","medium","tall"]])

    location_encoder = TargetEncoder()

    balcony_scaler = MinMaxScaler()

    ownership_encoder = OneHotEncoder(sparse_output = False,handle_unknown = 'ignore')

    missingindicator_ownership_encoder = OneHotEncoder(drop = 'first',sparse_output = False,handle_unknown = 'ignore')

    facing_encoder_union = FeatureUnion(
        transformer_list=[
            ("facing_onehot",OneHotEncoder(sparse_output = False,handle_unknown = 'ignore')),
            ("facing_target",TargetEncoder())
        ]
    )

    missingindicator_facing_encoder = OneHotEncoder(drop = 'first',sparse_output = False,handle_unknown = 'ignore')

    overlooking_garden_encoder = OneHotEncoder(sparse_output = False,handle_unknown = 'ignore')

    overlooking_mainroad_encoder = OneHotEncoder(categories=[[ -1, 0, 1 ]], drop=[-1], sparse_output=False, handle_unknown='ignore')

    overlooking_pool_encoder = OneHotEncoder(categories=[[ -1, 0, 1 ]], drop=[-1], sparse_output=False, handle_unknown='ignore')

    parking_cover_encoder = OneHotEncoder(sparse_output = False,handle_unknown = 'ignore')
    
    has_parking_encoder = OneHotEncoder(categories = [["multiple","single","no parking"]],drop = [["no parking"]],sparse_output = False,handle_unknown = 'ignore')

    effective_area_scaler = RobustScaler()

    area_per_room_scaler = RobustScaler()

    column_transformer = ColumnTransformer(
        transformers=[
            ("transaction_transformer", transaction_transformer, ["transaction"]),
            ("num_bhk_scaler", num_bhk_scaler, ["num_bhk"]),
            ("house_size_encoder", house_size_encoder, ["house_size"]),
            ("bathroom_scaler", bathroom_scaler, ["bathroom"]),
            ("bathroom_num_encoder", bathroom_num_encoder, ["bathroom_num"]),
            ("furnishing_encoder", furnishing_encoder, ["furnishing"]),
            ("floor_num_scaler", floor_num_scaler, ["floor_num"]),
            ("floor_height_encoder", floor_height_encoder, ["floor_height"]),
            ("num_floors_scaler", num_floors_scaler, ["num_floors"]),
            ("building_height_encoder", building_height_encoder, ["building_height"]),
            ("location_encoder", location_encoder, ["location"]),
            ("balcony_scaler", balcony_scaler, ["balcony"]),
            ("ownership_encoder", ownership_encoder, ["ownership"]),
            ("missingindicator_ownership_encoder", missingindicator_ownership_encoder, ["missingindicator_ownership"]),
            ("facing_encoder_union", facing_encoder_union, ["facing"]),
            ("missingindicator_facing_encoder", missingindicator_facing_encoder, ["missingindicator_facing"]),
            ("overlooking_garden_encoder", overlooking_garden_encoder, ["overlooking_garden"]),
            ("overlooking_mainroad_encoder", overlooking_mainroad_encoder, ["overlooking_mainroad"]),
            ("overlooking_pool_encoder", overlooking_pool_encoder, ["overlooking_pool"]),
            ("parking_cover_encoder", parking_cover_encoder, ["parking_cover"]),
            ("has_parking_encoder", has_parking_encoder, ["has_parking"]),
            ("effective_area_scaler", effective_area_scaler, ["effective_area"]),
            ("area_per_room_scaler", area_per_room_scaler, ["area_per_room"]),
        ]
    )
    

    return column_transformer







