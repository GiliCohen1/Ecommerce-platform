import json
import logging
from typing import Optional

import redis

from app.config import settings

logger = logging.getLogger(__name__)

_client: Optional[redis.Redis] = None


def get_client() -> Optional[redis.Redis]:
    global _client
    if _client is None:
        try:
            _client = redis.from_url(settings.redis_url, decode_responses=True)
            _client.ping()
        except redis.RedisError as e:
            logger.warning("Redis unavailable: %s", e)
            _client = None
    return _client


def cache_get(key: str) -> Optional[str]:
    client = get_client()
    if client is None:
        return None
    try:
        return client.get(key)
    except redis.RedisError as e:
        logger.warning("Redis GET failed for key %s: %s", key, e)
        return None


def cache_set(key: str, value: str, ttl: int) -> None:
    client = get_client()
    if client is None:
        return
    try:
        client.setex(key, ttl, value)
    except redis.RedisError as e:
        logger.warning("Redis SET failed for key %s: %s", key, e)


def redis_status() -> str:
    client = get_client()
    if client is None:
        return "unavailable"
    try:
        client.ping()
        return "connected"
    except redis.RedisError:
        return "unavailable"
