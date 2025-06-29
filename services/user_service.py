from typing import Optional
from dtos.user import user as user_dto
from repositories.user_repository import user_repository, repository

class user_service:
    def __init__(self, repository: user_repository):
        self.repository = repository

    async def create_user(self, model: user_dto) -> Optional[user_dto] | None:
        return await self.repository.create_user(model)
    
    async def delete_user(self, username) -> Optional[bool]:
        return await self.repository.delete_user(username)
    
    async def search_user(self, username) -> Optional[bool]:
        return await self.repository.search_user(username)
    
    async def validate_password(self, username,password):
        return await self.repository.validate_password(username, password)
    
def ret_user_service() -> user_service:
    return user_service(repository)

