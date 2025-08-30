import pandas as pd
from typing import Tuple,Optional
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

def give_best_model(model_pipeline: Pipeline, existing_model_pipeline: Optional[Pipeline], preprocessed_dfs: Tuple[pd.DataFrame, pd.DataFrame])-> Pipeline:
    
    if existing_model_pipeline:
        train_df,test_df = preprocessed_dfs
        X_train = train_df.drop(columns = ["remainder__amount"])
        y_train = train_df.remainder__amount.copy()
        X_test = test_df.drop(columns = ["remainder__amount"])
        y_test = test_df.remainder__amount.copy()

        y_train_pred_model = model_pipeline.predict(X_train)
        y_train_pred_existing_model = existing_model_pipeline.predict(X_train)
        y_test_pred_model = model_pipeline.predict(X_test)
        y_test_pred_existing_model = existing_model_pipeline.predict(X_test)

        model_train_mae = mean_absolute_error(y_train, y_train_pred_model)
        model_test_mae = mean_absolute_error(y_test, y_test_pred_model)
        model_overfit_penalty = abs(model_train_mae - model_test_mae)
        model_adjusted_test_mae = model_test_mae + model_overfit_penalty

        existing_model_train_mae = mean_absolute_error(y_train, y_train_pred_existing_model)
        existing_model_test_mae = mean_absolute_error(y_test, y_test_pred_existing_model)
        existing_model_overfit_penalty = abs(existing_model_train_mae - existing_model_test_mae)
        existing_model_adjusted_test_mae = existing_model_test_mae + existing_model_overfit_penalty

        if model_adjusted_test_mae < existing_model_adjusted_test_mae:
            return model_pipeline
        else:
            return existing_model_pipeline
    else:
        return model_pipeline

