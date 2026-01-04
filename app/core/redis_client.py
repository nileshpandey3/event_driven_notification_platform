"""
Establish a redis client connection to a redis server running locally via docker
"""

import redis

pool = redis.ConnectionPool(host="localhost", port=6379, decode_responses=True)
redis_client = redis.Redis(connection_pool=pool)
