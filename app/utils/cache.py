import logging

import redis as r

logger = logging.getLogger(__name__)

redis = None

def connect_redis():
    global redis
    redis = r.Redis(host='redis', port=6379)
    try:
        redis.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.error(f"Redis connection error: {e}")

def disconnect_redis():
    redis.close()


def cache(key_func, serializer, deserializer):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if redis is None:
                return func(*args, **kwargs)

            cache_key = key_func(*args, **kwargs)
            cached_result = redis.get(cache_key)
            if cached_result:
                return deserializer(cached_result)

            result = func(*args, **kwargs)
            if not isinstance(result, tuple):
                redis.set(cache_key, serializer(result))
            else:
                redis.set(cache_key, serializer(*result))
            return result

        return wrapper
    return decorator


