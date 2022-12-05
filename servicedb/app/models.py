from sqlalchemy import (
    Column,
    Table,
    Integer,
    String,
)
from .database import metadata


messages = Table(
    "messages",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("surname", String(30)),
    Column("name", String(30)),
    Column("patronymic", String(30)),
    Column("phone", String(30)),
    Column("message", String(255)),
)
