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


def call_history(method: Callable) -> Callable:
    """call details of method"""
    @wraps(method)
    def wrapper_function(self, *args, **kwargs) -> Any:
        """return output"""
        input_k = "{}:inputs".format(method.__qualname__)
        output_k = "{}:outputs".format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_k, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_k, output)
        return output
    return wrapper_function


def replay(fn: Callable) -> None:
    """display call history"""
    if fn is None or not hasattr(fn, "__self__"):
        return
    redis_s = getattr(fn.__self__, "_redis", None)
    if not isinstance(redis_s, redis.Redis):
        return
    fn_name = fn.__qualname__
    input_k = "{}:inputs".format(fn_name)
    output_k = "{}:outputs".format(fn_name)
    counter = 0
    if redis_s.exists(fn_name) != 0:
        counter = int(redis_s.get(fn_name))
    print("{} was called {} times:".format(fn_name, counter))
    fn_inputs = redis_s.lrange(input_k, 0, -1)
    fn_outputs = redis_s.lrange(output_k, 0, -1)
    for fn_input, fn_output in zip(fn_inputs, fn_outputs):
        print("{}(*{}) -> {}".format(
            fn_name,
            fn_input.decode("UTF-8"),
            fn_output,
        ))


class Cache:
    """Storaging data in a Redis data storage"""
    def __init__(self) -> None:
        """initilisation of instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
