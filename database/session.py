from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from typing import Callable

Base = declarative_base()
engine = create_engine('sqlite:///local.db')
session_maker = sessionmaker(engine, expire_on_commit=False)
session = session_maker()

def connection(func: Callable):
    def wraper(*args, **kwargs):
        with args[0].session:
            try: 
                return func(*args, **kwargs)
            except Exception as e:
                args[0].session.rollback()
                raise e
            finally:
                args[0].session.close()
    return wraper