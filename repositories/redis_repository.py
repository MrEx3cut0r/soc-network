from dtos.user import user as User
from typing import Optional
from dtos.post import Post
import redis
import pickle

class redis_repository():
    def __init__(self, client: redis.Redis):
        self.client = client
        
    def set(self, key, object):
        pickled = pickle.dumps(object)
        self.client.set(key, pickled)
        self.client.expire(key, 60*3)
        return object
        
    def get(self, key):
        pickled = self.client.get(key)
        return pickle.loads(pickled) if pickled else None
        
    def delete(self, key):
        return self.client.delete(key)
        