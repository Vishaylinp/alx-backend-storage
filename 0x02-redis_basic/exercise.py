#!/usr/bin/env python3
"""writing strings to Redis"""
import redis
import uuid
from typing import Union


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
