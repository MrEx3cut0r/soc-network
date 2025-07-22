from repositories.post_repository import post_repository, get_post_repository
from dtos.post import Post
from typing import Optional, List


class post_service():
    def __init__(self, repository: post_repository) -> None:
        self.repository = repository
    
    def create(self, post: Post) -> Optional[Post] | None:
        return self.repository.create(post)
    
    def delete(self, id: int) -> Optional[bool] | None:
        return self.repository.delete(id)
        
    def findByUsername(self, username: str) -> List[Post]:
        return self.repository.findByUsername(username)
        
    def findById(self, id: int) -> Optional[Post]:
        return self.repository.findById(id)
    
def ret_post_service() -> post_service:
    return post_service(get_post_repository())