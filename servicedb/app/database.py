import databases
import sqlalchemy


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@db:5432/db_msg"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)
