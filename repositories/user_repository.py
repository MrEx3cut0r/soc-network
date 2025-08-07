from database.session import connection, session
from tables.user_table import user_table
from dtos.user import user as user_dto
from typing import Optional
from fastapi import HTTPException
from cryptography.fernet import Fernet
from config import secret_key
from repositories.redis_repository import redis_repository
from database.redis_enter import client
from dtos.subscribe import subscribe
from tables.subscribers_table import subscribers_table

fernet = Fernet(secret_key.encode())
class user_repository:
    def __init__(self, session):
        self.session = session
        self.RedisClient = redis_repository(client)
        
    @connection
    def create_user(self, model: user_dto) -> Optional[user_dto] | None:
        model.password = fernet.encrypt(model.password.encode())
        new_user = user_table(**model.dict())
        self.session.add(new_user)
        self.session.commit()
        return model
        
    @connection
    def delete_user(self, username: str) -> Optional[bool] | None:
        user = self.session.query(user_table).filter_by(username=username).first()
        redis_user = self.RedisClient.get(username)
        if redis_user:
            self.RedisClient.delete(username)   
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        raise HTTPException(status_code=404, detail="user not found")
        
    @connection
    def search_user(self, username: str) -> Optional[user_dto] | bool:
        redis_user = self.RedisClient.get(username)
        if redis_user:
            return redis_user
        user = self.session.query(user_table).filter_by(username=username).first()
        if user:
            self.RedisClient.set(username, user)
            return user
        return False
        
    @connection
    def validate_password(self, username, password) -> Optional[bool] | None:
        user = self.RedisClient.get(username)
        if not user:
            user = self.session.query(user_table).filter_by(username=username).first()
        if user:
            self.RedisClient.set(user.username, user)
            if fernet.decrypt(user.password).decode() == password:
                return True
            return False  
            
        raise HTTPException(status_code=404, detail='user not found')

def ret_user_repository() -> user_repository:
    return user_repository(session)