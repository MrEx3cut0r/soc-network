from dtos.user import user as User
from typing import Optional
import redis
import pickle

class redis_repository():
    def __init__(self, client: redis.Redis):
        self.client = client
        
    def set_user(self, user: User) -> User:
        pickled = pickle.dumps(user)
        self.client.set(user.username, pickled)
        self.client.expire(user.username, 60*3)
        return user
        
    def get_user(self, username: str) -> Optional[User] | None:
        pickled = self.client.get(username)
        return pickle.loads(pickled) if pickled else None
        
    def delete(self, username: str):
        return self.client.delete(username)