from pydantic import BaseModel
from tables.posts_table import posts_table


class Post(BaseModel):
    username: str
    text: str
    when: str
    