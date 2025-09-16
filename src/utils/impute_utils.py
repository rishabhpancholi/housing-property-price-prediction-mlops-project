import sklearn
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator,TransformerMixin

# Setting sklearn config to pandas
sklearn.set_config(transform_output='pandas')

def get_imputer_object()-> Pipeline:
        # Function to rename the columns before putting back into imputation pipeline
        def prefix_remover(X, prefixes):

            prefix_list = [f"{prefix}__" for prefix in prefixes]
            new_cols = X.columns
            
            for prefix in prefix_list:
                new_cols = [col.replace(prefix,"") if col.startswith(prefix) else col for col in new_cols]

            return X.rename(
                columns = dict(zip(X.columns,new_cols))
            )

        # imputer to impute bathroom values based on num_bhk
        class GroupAggregateImputer(BaseEstimator, TransformerMixin):

            def __init__(self,variable,group_col,estimator,add_indicator = False):
                self.variable = variable
                self.group_col = group_col
                self.estimator = estimator
                self.add_indicator = add_indicator

            def fit(self,X,y = None):

                self.group_medians_ = {}
                self.group_modes_ = {}

                if self.estimator == "median":
                        self.group_medians_[self.variable] =  X.groupby(self.group_col)[self.variable].median()
                        
                elif self.estimator == "mode":
                        self.group_modes_[self.variable] =  X.groupby(self.group_col)[self.variable].agg(lambda x: x.mode().iloc[0])
                    
                return self

            def transform(self,X):
                X = X.copy()

                if self.add_indicator:
                    X = X.assign(**{
                        f"{self.variable}_missingindicator" : lambda df:(
                                np.where(
                                    df[self.variable].isnull(),
                                    1,0
                                )
                            )
                    })

                if self.estimator == "median":
                        mask = X[self.variable].isnull()
                        X.loc[mask,self.variable] = X.loc[mask,self.group_col].map(self.group_medians_[self.variable])
                        
                elif self.estimator == "mode":
                        mask = X[self.variable].isnull()
                        X.loc[mask,self.variable] = X.loc[mask,self.group_col].map(self.group_modes_[self.variable]) 

                
                return X

        furnishing_imputer = ColumnTransformer(transformers = [
            ("furnishing_imputer",GroupAggregateImputer(variable = "furnishing",group_col = "transaction",estimator = "mode"),["furnishing","transaction"])
        ],remainder = "passthrough")

        furnishing_imputation_pipeline = Pipeline(steps = [
            ("furnishing_imputer",furnishing_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["furnishing_imputer","remainder"]}))
        ])

        floor_num_imputer = ColumnTransformer(transformers = [
            ("floor_num_imputer",SimpleImputer(strategy = "median"),["floor_num"])
        ],remainder = "passthrough")

        floor_num_imputation_pipeline = Pipeline(steps = [
            ("floor_num_imputer",floor_num_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["floor_num_imputer","remainder"]}))
        ])

        num_floors_imputer = ColumnTransformer(transformers = [
            ("num_floors_imputer",GroupAggregateImputer(variable = "num_floors",group_col = "floor_num",estimator = "median"),["num_floors","floor_num"])
        ],remainder = "passthrough")

        num_floors_imputation_pipeline = Pipeline(steps = [
            ("num_floors_imputer",num_floors_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["num_floors_imputer","remainder"]}))
        ])

        balcony_imputer = ColumnTransformer(transformers = [
            ("balcony_imputer", GroupAggregateImputer(variable = "balcony",group_col = "num_bhk",estimator = "median", add_indicator = True),["balcony","num_bhk"])
        ],remainder = "passthrough")

        balcony_imputation_pipeline = Pipeline(steps = [
            ("balcony_imputer",balcony_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["balcony_imputer","remainder"]}))
        ])

        ownership_imputer = ColumnTransformer(transformers = [
            ("ownership_imputer",SimpleImputer(strategy = 'most_frequent',add_indicator = True),["ownership"])
        ], remainder = "passthrough")


        ownership_imputation_pipeline = Pipeline(steps = [
            ("ownership_imputer",ownership_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["ownership_imputer","remainder"]}))
        ])

        facing_imputer = ColumnTransformer(transformers = [
            ("facing_imputer",SimpleImputer(strategy = 'constant',fill_value = 'Missing',add_indicator = True),["facing"])
        ], remainder = "passthrough")

        facing_imputation_pipeline = Pipeline(steps = [
            ("facing_imputer",facing_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["facing_imputer","remainder"]}))
        ])

        overlooking_garden_imputer = ColumnTransformer(transformers = [
            ("overlooking_garden_imputer",SimpleImputer(strategy = 'constant',fill_value = -1),["overlooking_garden"])
        ], remainder = "passthrough")

        overlooking_garden_imputation_pipeline = Pipeline(steps = [
            ("overlooking_garden_imputer",overlooking_garden_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["overlooking_garden_imputer","remainder"]}))
        ])

        overlooking_mainroad_imputer = ColumnTransformer(transformers = [
            ("overlooking_mainroad_imputer",SimpleImputer(strategy = 'constant',fill_value = -1),["overlooking_mainroad"])
        ], remainder = "passthrough")

        overlooking_mainroad_imputation_pipeline = Pipeline(steps = [
            ("overlooking_mainroad_imputer",overlooking_mainroad_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["overlooking_mainroad_imputer","remainder"]}))
        ])

        overlooking_pool_imputer = ColumnTransformer(transformers = [
            ("overlooking_pool_imputer",SimpleImputer(strategy = 'constant',fill_value = -1),["overlooking_pool"])
        ], remainder = "passthrough")

        overlooking_pool_imputation_pipeline = Pipeline(steps = [
            ("overlooking_pool_imputer",overlooking_pool_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["overlooking_pool_imputer","remainder"]}))
        ])

        parking_cover_imputer =  ColumnTransformer(transformers = [
            ("parking_cover_imputer",SimpleImputer(strategy = 'constant',fill_value = "No parking"),["parking_cover"])
        ],remainder = "passthrough")

        parking_cover_imputation_pipeline = Pipeline(steps = [
            ("parking_cover_imputer",parking_cover_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["parking_cover_imputer","remainder"]}))
        ])

        parking_spots_imputer =  ColumnTransformer(transformers = [
            ("parking_spots_imputer",SimpleImputer(strategy = 'constant',fill_value = 0),["parking_spots"])
        ],remainder = "passthrough")

        parking_spots_imputation_pipeline = Pipeline(steps = [
            ("parking_spots_imputer",parking_spots_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["parking_spots_imputer","remainder"]}))
        ])

        carpet_area_imputer =  ColumnTransformer(transformers = [
            ("carpet_area_imputer",SimpleImputer(strategy = 'constant',fill_value = -1),["carpet_area"])
        ],remainder = "passthrough")

        carpet_area_imputation_pipeline = Pipeline(steps = [
            ("carpet_area_imputer",carpet_area_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["carpet_area_imputer","remainder"]}))
        ])

        super_area_imputer =  ColumnTransformer(transformers = [
            ("super_area_imputer",SimpleImputer(strategy = 'constant',fill_value = -1),["super_area"])
        ],remainder = "passthrough")

        super_area_imputation_pipeline = Pipeline(steps = [
            ("super_area_imputer",super_area_imputer),
            ("prefix_remover",FunctionTransformer(func = prefix_remover, kw_args = {"prefixes" : ["super_area_imputer","remainder"]}))
        ])

        imputation_pipeline = Pipeline(steps = [
            ("furnishing_imputation_pipeline",furnishing_imputation_pipeline),
            ("floor_num_imputation_pipeline",floor_num_imputation_pipeline),
            ("num_floors_imputation_pipeline",num_floors_imputation_pipeline),
            ("balcony_imputation_pipeline",balcony_imputation_pipeline),
            ("ownership_imputation_pipeline",ownership_imputation_pipeline),
            ("facing_imputation_pipeline",facing_imputation_pipeline),
            ("overlooking_garden_imputation_pipeline",overlooking_garden_imputation_pipeline),
            ("overlooking_mainroad_imputation_pipeline",overlooking_mainroad_imputation_pipeline),
            ("overlooking_pool_imputation_pipeline",overlooking_pool_imputation_pipeline),
            ("parking_cover_imputation_pipeline",parking_cover_imputation_pipeline),
            ("parking_spots_imputation_pipeline",parking_spots_imputation_pipeline),
            ("carpet_area_imputation_pipeline",carpet_area_imputation_pipeline),
            ("super_area_imputation_pipeline",super_area_imputation_pipeline)
        ])

        return imputation_pipeline
