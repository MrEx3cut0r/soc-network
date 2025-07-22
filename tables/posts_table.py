from sqlalchemy import Column, String, Integer
from database.session import Base


class posts_table(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    text = Column(String, nullable=False)
    when = Column(String, nullable=False)
    
    def __repr__(self):
        return f"by {username}, {when}\n{text}"
        
       