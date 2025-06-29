from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import Callable

Base = declarative_base()
engine = create_async_engine('postgresql+asyncpg:///db.db')
session_maker = async_sessionmaker(engine, expire_on_commit=False)
session = session_maker()

async def connection(func: Callable):
    async def wraper(*args, **kwargs):
        async with args[0].session:
            try: 
                return await func(*args, **kwargs)
            except Exception as e:
                await args[0].session.rollback()
                raise e
            finally:
                await args[0].session.close()