import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:password@db:5432/db_msg"

metadata = sqlalchemy.MetaData()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
