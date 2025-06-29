from database.session import connection, session
from tables.user_table import user_table
from dtos.user import user as user_dto
from typing import Optional
from fastapi import HTTPException
from cryptography.fernet import Fernet
import os

key = str(os.environ['secrey_key'])
fernet = Fernet(key)

class user_repository:
    async def __init__(self, session) -> None:
        self.session = session
    
    async def create_user(self, model: user_dto) -> Optional[user_dto] | None:
        model.password = fernet.encrypt(model.password)
        await self.session.add(model)
        await self.session.commit()
        return model
    
    async def delete_user(self, username: str) -> Optional[bool]:
        user = await self.session.query(user_table).filter_by(username=username).first()

        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        
        raise HTTPException(status_code=404, detail="user not found")

    async def search_user(self, username: str) -> Optional[user_dto]:
        user = await self.session.query(user_table).filter_by(username=username).first()

        if user:
            return user
        
        raise HTTPException(status_code=404, detail="user not found")
    
    async def validate_password(self, username, password) -> Optional[bool]:
        user = await self.session.query(user_table).filter_by(username=username).first()
        if user:
            if fernet.decrypt(user.password) == password:
                return True
            return False
        
        raise HTTPException(status_code=404, detail='user not found')

repository = user_repository(session)