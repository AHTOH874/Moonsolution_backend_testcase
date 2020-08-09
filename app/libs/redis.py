import redis


Redis = redis.StrictRedis(host='redis', port=6379, db=1, password="REDIS_PASSWORD")
