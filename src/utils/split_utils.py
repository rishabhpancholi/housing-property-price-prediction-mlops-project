import pandas as pd
from typing import Tuple
from sklearn.model_selection import train_test_split

# Function to split dataset

def split_data(df: pd.DataFrame, test_ratio: float, val_ratio: float, test_random_state: int, val_random_state: int)-> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Function to split dataset

    """
    X = df.drop(columns = ["amount"])
    y = df.amount.copy()

    X_,X_test,y_,y_test = train_test_split(X,y,test_size = test_ratio,random_state= test_random_state)
    X_train,X_val,y_train,y_val = train_test_split(X_,y_,test_size = val_ratio,random_state = val_random_state)

    train_df = X_train.join(y_train)
    val_df = X_val.join(y_val)
    test_df = X_test.join(y_test)

    return (train_df,val_df,test_df)

