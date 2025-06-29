from database.session import Base
from sqlalchemy import Column, String, Integer
class user_table(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return {'id': id,
                'username': self.username,
                'email': self.email}