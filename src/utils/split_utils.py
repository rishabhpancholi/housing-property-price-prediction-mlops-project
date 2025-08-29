import pandas as pd
from typing import Tuple
from sklearn.model_selection import train_test_split

# Function to split dataset

def split_data(df: pd.DataFrame, test_size: float, random_state: int)-> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Function to split dataset

    """
    X = df.drop(columns = ["amount"])
    y = df.amount.copy()

    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = test_size,random_state= random_state)

    train_df = X_train.join(y_train)
    test_df = X_test.join(y_test)

    return (train_df, test_df)

