import mlflow
import dagshub
import numpy as np
import pandas as pd
from typing import Tuple,Dict
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import TransformedTargetRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import FunctionTransformer
from sklearn.metrics import mean_absolute_error,root_mean_squared_error,r2_score
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor,AdaBoostRegressor
from feature_engine.selection import SelectBySingleFeaturePerformance,SmartCorrelatedSelection


# Function to train, evaluate and register the model
def train_and_evaluate(repo_owner: str,repo_name: str,mlflow_tracking_uri: str,regressor_name: str,target_transformer_name: str, drop_correlated_threshold: float, feature_selector_threshold: float, model_hyperparams: Dict, preprocessed_dfs: Tuple[pd.DataFrame, pd.DataFrame])-> Pipeline:

    mlflow.set_tracking_uri(mlflow_tracking_uri)
    dagshub.init(repo_owner = repo_owner, repo_name = repo_name, mlflow=True)
    mlflow.set_experiment(repo_name)

    
    with mlflow.start_run():
        model_mapper = {
            "GradientBoostingRegressor": GradientBoostingRegressor,
            "RandomForestRegressor": RandomForestRegressor,
            "AdaBoostRegressor": AdaBoostRegressor,
            "XGBRegressor": XGBRegressor,
            "DecisionTreeRegressor": DecisionTreeRegressor
        }

        target_transformer_mapper = {
            "log": FunctionTransformer(func = np.log, inverse_func = np.exp),
            "cbrt": FunctionTransformer(func = np.cbrt, inverse_func = lambda x: x**3),
            "sqrt": FunctionTransformer(func = np.sqrt, inverse_func = lambda x: x**2),
            "same": FunctionTransformer(func = lambda x:x, inverse_func = lambda x:x)
        }

        train_df, test_df = preprocessed_dfs

        drop_correlated = SmartCorrelatedSelection(
            threshold = drop_correlated_threshold, 
            selection_method = 'model_performance', 
            estimator = DecisionTreeRegressor(), 
            scoring = 'r2'                                      
        )
        mlflow.log_param("drop_correlated_threshold", drop_correlated_threshold)
        
        feature_selector = SelectBySingleFeaturePerformance(
            estimator = DecisionTreeRegressor(),
            scoring = 'r2',
            threshold = feature_selector_threshold
        )
        mlflow.log_param("feature_selector_threshold", feature_selector_threshold)

        model = TransformedTargetRegressor(
            regressor = model_mapper.get(regressor_name)(**model_hyperparams),
            transformer = target_transformer_mapper.get(target_transformer_name)
        )
        mlflow.log_param("regressor", regressor_name)
        mlflow.log_param("target_transformer", target_transformer_name)

        model_pipeline = Pipeline(steps = [
            ("drop_correlated",drop_correlated),
            ("feature_selector",feature_selector),
            ("model", model)
        ])

        X_train = train_df.drop(columns = "amount")
        y_train = train_df.amount.copy()
        model_pipeline.fit(X_train, y_train)


        X_test = test_df.drop(columns = "amount")
        y_test = test_df.amount.copy()

        y_train_pred = model_pipeline.predict(X_train)
        y_test_pred = model_pipeline.predict(X_test)

        train_mae = mean_absolute_error(y_train, y_train_pred)
        train_rmse = root_mean_squared_error(y_train, y_train_pred)
        train_r2 = r2_score(y_train, y_train_pred)
        
        train_metrics = {
            "train_mae" : train_mae,
            "train_rmse" : train_rmse,
            "train_r2": train_r2
        }
        mlflow.log_metrics(train_metrics)

        test_mae = mean_absolute_error(y_test, y_test_pred)
        test_rmse = root_mean_squared_error(y_test, y_test_pred)
        test_r2 = r2_score(y_test, y_test_pred)

        test_metrics = {
            "test_mae" : test_mae,
            "test_rmse" : test_rmse,
            "test_r2" : test_r2
        }
        mlflow.log_metrics(test_metrics)

    return model_pipeline
    

