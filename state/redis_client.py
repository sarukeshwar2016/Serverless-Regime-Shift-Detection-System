"""
Redis client — manages real-time state and caching for the platform.
"""

import os
from typing import Any, Optional

import redis
from dotenv import load_dotenv

load_dotenv()


class RedisClient:
    """Simple Redis wrapper for state management and caching."""

    def __init__(self):
        self._client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True,
        )

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a key-value pair with an optional TTL in seconds."""
        self._client.set(key, str(value), ex=ttl)

    def get(self, key: str) -> Optional[str]:
        """Get a value by key."""
        return self._client.get(key)

    def delete(self, key: str) -> None:
        """Delete a key."""
        self._client.delete(key)

    def ping(self) -> bool:
        """Check if Redis is reachable."""
        try:
            return self._client.ping()
        except redis.ConnectionError:
            return False
