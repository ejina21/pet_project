from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import NullPool
from app.config import settings


if settings.MODE == "TEST":
    DATABASE_URL = str(settings.test_database_url)
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = str(settings.database_url)
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
