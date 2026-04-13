"""
Establish a redis client connection to a redis server running locally via docker
"""

import os

import redis

pool = redis.ConnectionPool(
    host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True
)
redis_client = redis.Redis(connection_pool=pool)
