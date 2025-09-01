import json
import redis
from api.core.config import AppConfig

# App Config
config = AppConfig()

# Setting up redis
redis_client = redis.Redis.from_url(config.redis_url)

# Function to get cached predictions from redis
def get_cached_prediction(key: str):
    """
    Returns cached predictions if the corresponding key exists in redis cache

    """
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None 


# Function to set cached predictions in redis
def set_cached_prediction(key: str, value: dict, expiry_time: int = 3600):
    """
    Sets cached predictions in redis

    """
    redis_client.setex(key, expiry_time, json.dumps(value))