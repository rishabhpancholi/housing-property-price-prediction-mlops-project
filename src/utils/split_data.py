import numpy as np
import pandas as pd
from zlib import crc32
from typing import Tuple

def test_set_check(identifier: int, test_ratio: float)->bool:
    return crc32(np.int64(identifier)) & 0xffffffff < test_ratio * 2**32

def train_test_split(df: pd.DataFrame, test_ratio: float, id_col: str = "index")->Tuple[pd.DataFrame, pd.DataFrame]:
    ids = df[id_col]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
    return df.loc[~in_test_set],df.loc[in_test_set]