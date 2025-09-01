import pandas as pd
from api.core.config import AppConfig
from api.model.load_model import load_model
from api.cache.redis_cache import get_cached_prediction,set_cached_prediction

# App Config
config = AppConfig()

# Loading the model pipeline
model_pipeline = load_model(config)

def get_prediction(data: dict)-> dict:
    """
    Returns prediction for the given data

    """
    input_data = pd.DataFrame([data])

    cache_key = [str(val) for val in data.values()]
    cache_key = "-".join(cache_key)

    cached_prediction = get_cached_prediction(cache_key)

    if cached_prediction is not None:
        return cached_prediction

    prediction = model_pipeline.predict(input_data)[0]
    set_cached_prediction(cache_key, prediction)
    return prediction