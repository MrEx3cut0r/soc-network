from dtos.post import Post
from database.session import connection
from typing import Optional, List
from tables.posts_table import posts_table
from database.session import session

class post_repository():
    def __init__ (self, session) -> None:
        self.session = session
    
    @connection
    def create(self, post: Post) -> Optional[Post]:
        # giving 'post' arguments to posts_table using '**'
        print(post)
        self.session.add(posts_table(**post.dict()))
        self.session.commit()
        return post
    @connection
    def delete(self, id: int) -> Optional[bool]:
        found_post = self.session.query(posts_table).filter_by(id=id).first()
        if found_post:
            self.session.delete(found_post)
            self.session.commit()
            return True
        return False
    """
    @connection
    def findByUsername(self, username: str) -> List[Post]:
        posts = self.session.query(posts_tables).filter_by(username=username).all()
        return posts
    """
    @connection
    def findById(self, id: int) -> Optional[Post]:
        post = self.session.query(posts_table).filter_by(id=id).first()
        if post:
           return post
        return False

def get_post_repository() -> post_repository:
    return post_repository(session)