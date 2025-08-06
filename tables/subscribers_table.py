from database.session import Base
from sqlalchemy import Column, String, Integer, JSON

class subscribers_table(Base):
	__tablename__ = "subscribers"
	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True)
	subscribers = Column(JSON)

	def __repr__(self):
		return f"id: {self.id}\nusername: {self.username}\nsubscribers: {self.subscribers}"


