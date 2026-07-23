import json
import logging
import time
from typing import Optional

import redis

from app.config import settings

logger = logging.getLogger(__name__)

_client: Optional[redis.Redis] = None
_retry_after: float = 0  # monotonic timestamp — don't attempt Redis before this


def get_client() -> Optional[redis.Redis]:
    global _client, _retry_after

    if _client is not None:
        return _client

    # Circuit breaker: skip reconnect attempts during the cooldown window
    if time.monotonic() < _retry_after:
        return None

    try:
        _client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_connect_timeout=1,  # fail fast instead of waiting for OS timeout
        )
        _client.ping()
        logger.info("Redis connected at %s", settings.redis_url)
    except redis.RedisError as e:
        logger.warning("Redis unavailable: %s — will retry in 30s", e)
        _client = None
        _retry_after = time.monotonic() + 30  # back off for 30 seconds

    return _client


def cache_get(key: str) -> Optional[str]:
    client = get_client()
    if client is None:
        return None
    try:
        return client.get(key)
    except redis.RedisError as e:
        logger.warning("Redis GET failed for key %s: %s", key, e)
        _mark_client_dead()
        return None


def cache_set(key: str, value: str, ttl: int) -> None:
    client = get_client()
    if client is None:
        return
    try:
        client.setex(key, ttl, value)
    except redis.RedisError as e:
        logger.warning("Redis SET failed for key %s: %s", key, e)
        _mark_client_dead()


def redis_status() -> str:
    client = get_client()
    if client is None:
        return "unavailable"
    try:
        client.ping()
        return "connected"
    except redis.RedisError:
        _mark_client_dead()
        return "unavailable"


def _mark_client_dead() -> None:
    global _client, _retry_after
    _client = None
    _retry_after = time.monotonic() + 30
