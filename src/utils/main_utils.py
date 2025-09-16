import yaml
import joblib
import pandas as pd
from pathlib import Path
from typing import Union
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

def read_data(file_path: Path)-> pd.DataFrame:
    return pd.read_csv(file_path)

def read_yaml_file(file_path: Path)-> dict:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
def save_joblib_file(file_path: Path, obj: Union[Pipeline, ColumnTransformer]):
    with open(file_path, 'wb') as file:
        return joblib.dump(obj,file) 