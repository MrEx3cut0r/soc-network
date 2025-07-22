from typing import Optional
from dtos.user import user as user_dto
from repositories.user_repository import user_repository, ret_user_repository
class user_service:
    def __init__(self, repository: user_repository):
        self.repository = repository

    def create_user(self, model: user_dto) -> Optional[user_dto] | None:
        return self.repository.create_user(model)
    
    def delete_user(self, username) -> Optional[bool]:
        return self.repository.delete_user(username)
    
    def search_user(self, username) -> Optional[bool]:
        return self.repository.search_user(username)
    
    def validate_password(self, username,password):
        return self.repository.validate_password(username, password)
    
def ret_user_service() -> user_service:
    return user_service(ret_user_repository())

