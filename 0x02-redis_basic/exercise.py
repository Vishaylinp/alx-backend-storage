#!/usr/bin/env python3
"""writing strings to Redis"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any


def count_calls(method: Callable) -> Callable:
    """count number of calls in a method"""
    @wraps(method)
    def wrapper_function(self, *args, **kwargs) -> Any:
        """call method after increasing"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper_function


"""
def wrapper_function(self, *args, **kwargs) -> Any:
        input_k = "{}:inputs".format(method.__qualname__)
        output_k = "{}:outputs".format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_k, str(arg))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_k, output)
        return output
    return wrapper_function
"""


class Cache:
    """Storaging data in a Redis data storage"""
    def __init__(self) -> None:
        """initilisation of instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """takes data arguments"""
        r_key = str(uuid.uuid4())
        self._redis.set(r_key, data)
        return r_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Get value from Redis data storage"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Gets a string"""
        return self.get(key, lambda c: c.decode("UTF-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, lambda c: int(c))
