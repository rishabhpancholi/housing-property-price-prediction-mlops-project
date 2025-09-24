import pandas as pd
from typing import List
from sklearn.compose import ColumnTransformer

def debug_preprocessor(preprocessor: ColumnTransformer,df: pd.DataFrame)-> List[str]:
    errors = []
    for name,transformer,col in preprocessor.transformers_:
        try:
            subset = df[col]
            transformer.transform(subset)
        except Exception as e:
            errors.append(
                f"Transformer {transformer} failed on column {col} with error {repr(e)}"
            )
    
    return errors
