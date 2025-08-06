from pydantic import BaseModel

class subscribe(BaseModel):
	username: str
	subscribers: list