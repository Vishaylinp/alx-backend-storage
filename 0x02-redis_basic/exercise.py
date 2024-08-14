#!/usr/bin/env python3
"""writing strings to Redis"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    """Storaging data in a Redis data storage"""
    def __init__(self) -> None:
        """initilisation of instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
        return fn(data) if fn iss not None else data

    def get_str(self, key: str) -> str:
        """Gets a string"""
        return self.get(key, lambda c: c.decode("UTF-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, lambda c: int(c))
