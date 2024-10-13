import redis
import os

try:
    redis_client = redis.StrictRedis.from_url(os.getenv('REDIS_URL'))
    redis_client.ping()  # Check if Redis is accessible
    print("Connected to Redis!")
except redis.ConnectionError as e:
    print(f"Redis connection error: {e}")
