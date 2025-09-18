import optuna
import warnings
import numpy as np
import pandas as pd
from src.utils import *
from typing import Tuple
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import TransformedTargetRegressor
from sklearn.model_selection import cross_val_score,KFold
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor

# Ignore warnings
warnings.filterwarnings('ignore')

def train_model(X_train: pd.DataFrame,y_train: pd.Series,kfold_nsplits: int, optuna_ntrials: int)->Tuple[TransformedTargetRegressor,dict]:
              
            def objective(trial):
                regressor_name = trial.suggest_categorical(
                     "regressor",
                     ["XGBRegressor","LinearRegression","Ridge","Lasso","KNeighborsRegressor","RandomForestRegressor","AdaBoostRegressor","GradientBoostingRegressor"]
                )
                if regressor_name == "XGBRegressor":
                    n_estimators = trial.suggest_int("n_estimators", 50, 300)
                    learning_rate = trial.suggest_float("learning_rate", 0.001, 0.3, log=True)
                    max_depth = trial.suggest_int("max_depth", 2, 10)
                    subsample = trial.suggest_float("subsample", 0.5, 1.0)
                    colsample_bytree = trial.suggest_float("colsample_bytree", 0.5, 1.0)
                    regressor = XGBRegressor(
                        n_estimators=n_estimators,
                        learning_rate=learning_rate,
                        max_depth=max_depth,
                        subsample=subsample,
                        colsample_bytree=colsample_bytree,
                        n_jobs=-1
                    )
                elif regressor_name == "LinearRegression":
                    fit_intercept = trial.suggest_categorical("fit_intercept", [True, False])
                    regressor = LinearRegression(
                        fit_intercept=fit_intercept,
                        n_jobs=-1
                )
                elif regressor_name == "Ridge":
                    alpha = trial.suggest_float("alpha", 0.0001, 10.0, log=True)
                    fit_intercept = trial.suggest_categorical("fit_intercept", [True, False])
                    regressor = Ridge(
                        alpha=alpha,
                        fit_intercept=fit_intercept
                    )
                elif regressor_name == "Lasso":
                    alpha = trial.suggest_float("alpha", 0.0001, 1.0, log=True)
                    fit_intercept = trial.suggest_categorical("fit_intercept", [True, False])
                    regressor = Lasso(
                        alpha=alpha,
                        fit_intercept=fit_intercept
                    )
                elif regressor_name == "KNeighborsRegressor":
                    n_neighbors = trial.suggest_int("n_neighbors", 2, 30)
                    weights = trial.suggest_categorical("weights", ["uniform", "distance"])
                    p = trial.suggest_int("p", 1, 2)  
                    regressor = KNeighborsRegressor(
                        n_neighbors=n_neighbors,
                        weights=weights,
                        p=p,
                        n_jobs=-1
                    )
                elif regressor_name == "RandomForestRegressor":
                    n_estimators = trial.suggest_int("n_estimators", 50, 300)
                    max_depth = trial.suggest_int("max_depth", 2, 20)
                    min_samples_split = trial.suggest_int("min_samples_split", 2, 10)
                    max_features = trial.suggest_categorical("max_features", ["sqrt", "log2", None])
                    regressor = RandomForestRegressor(
                        n_estimators=n_estimators,
                        max_depth=max_depth,
                        min_samples_split=min_samples_split,
                        max_features=max_features,
                        n_jobs=-1
                    )
                elif regressor_name == "AdaBoostRegressor":
                    n_estimators = trial.suggest_int("n_estimators", 50, 300)
                    learning_rate = trial.suggest_float("learning_rate", 0.001, 2.0, log=True)
                    loss = trial.suggest_categorical("loss", ["linear", "square", "exponential"])
                    regressor = AdaBoostRegressor(
                        n_estimators=n_estimators,
                        learning_rate=learning_rate,
                        loss=loss
                    )
                elif regressor_name == "GradientBoostingRegressor":
                    n_estimators = trial.suggest_int("n_estimators", 50, 300)
                    subsample = trial.suggest_float("subsample", 0.5, 1.0)
                    learning_rate = trial.suggest_float("learning_rate", 0.001, 2.0, log=True)
                    min_samples_split = trial.suggest_int("min_samples_split", 2, 10)
                    max_depth = trial.suggest_int("max_depth", 2, 10)
                    max_features = trial.suggest_categorical("max_features", ["sqrt", "log2", None])
                    regressor = GradientBoostingRegressor(
                        n_estimators=n_estimators,
                        subsample=subsample,
                        learning_rate=learning_rate,
                        min_samples_split=min_samples_split,
                        max_depth=max_depth,
                        max_features=max_features
                    )
                

                target_transformer_name = trial.suggest_categorical(
                        "target_transformer",
                        ["log","cbrt","sqrt","same"]
                )

                if target_transformer_name == "log":
                    transformer = FunctionTransformer(
                        func=np.log,
                        inverse_func=np.exp
                )
                
                elif target_transformer_name == "cbrt":
                    transformer = FunctionTransformer(
                        func=np.cbrt,
                        inverse_func=lambda x:x**3
                )
        
                elif target_transformer_name == "sqrt":
                    transformer = FunctionTransformer(
                        func=np.sqrt,
                        inverse_func=lambda x:x**2
                )
        
                elif target_transformer_name == "same":
                    transformer = FunctionTransformer(
                        func=lambda x:x,
                        inverse_func=lambda x:x
                )
                        
                model = TransformedTargetRegressor(
                    regressor=regressor,
                    transformer=transformer
                )
                
                cv = KFold(n_splits = kfold_nsplits, shuffle = True, random_state = 42)

                scores = cross_val_score(
                        model,X_train,y_train,
                        scoring = "neg_mean_absolute_error",
                        cv = cv,
                        n_jobs = -1
                )

                mean_score = np.mean(scores)
                return mean_score
            
            study = optuna.create_study(direction="maximize")
            study.optimize(objective, n_trials=optuna_ntrials)

            best_params = study.best_params

            regressor = regressor_dict[best_params["regressor"]]
            transformer = transformer_dict[best_params["target_transformer"]]
            regressor_params = {k:v for k,v in best_params.items() if k!="target_transformer" and k!="regressor"}

            trained_model = TransformedTargetRegressor(
                 regressor=regressor(**regressor_params),
                 transformer=transformer
            )

            trained_model.fit(X_train,y_train)

            return (trained_model,best_params)

