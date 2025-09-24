import pandas as pd
from api.model import HouseFeatures
from sklearn.pipeline import Pipeline
from api.service import debug_preprocessor

# Function to give prediction
def give_prediction(house_features: HouseFeatures, model: Pipeline)->float:
    house_features_dict = house_features.model_dump()
    house_features_df = pd.DataFrame(house_features_dict,index=[0])
    num_features = [features for features in house_features_df.columns if house_features_df[features].dtypes != 'O']
    house_features_df[num_features] = house_features_df[num_features].astype(float)

    preprocessor = model.named_steps['preprocessor']
    errors = debug_preprocessor(preprocessor,house_features_df)
    if errors:   
      return errors[0]
    return model.predict(house_features_df)[0]