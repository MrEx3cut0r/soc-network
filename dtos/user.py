from pydantic import BaseModel

class user(BaseModel):
    username: str
    email: str
    password: str