import numpy as np
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import FunctionTransformer
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor

regressor_dict = {
  "XGBRegressor": XGBRegressor,
  "RandomForestRegressor": RandomForestRegressor,
  "AdaBoostRegressor": AdaBoostRegressor,
  "GradientBoostingRegressor": GradientBoostingRegressor,
  "DecisionTreeRegressor": DecisionTreeRegressor,
  "LinearRegression": LinearRegression,
  "KNeighborsRegressor": KNeighborsRegressor,
  "Lasso": Lasso,
  "Ridge": Ridge
}

def square(X):
    return X**2

def cube(X):
    return X**3

def same(X):
    return X

transformer_dict = {
  "log": FunctionTransformer(
      func=np.log,
      inverse_func=np.exp
  ),
  "sqrt": FunctionTransformer(
      func=np.sqrt,
      inverse_func=square
  ),
  "cbrt": FunctionTransformer(
      func=np.cbrt,
      inverse_func=cube
  ),
  "same": FunctionTransformer(
      func=same,
      inverse_func=same
  )
}