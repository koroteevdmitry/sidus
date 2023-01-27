import uuid
from typing import Optional

from sqlalchemy import Column, String, text
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )
    username: str = Field(sa_column=Column("username", String, unique=True))
    password: str
    email: str = Field(sa_column=Column("email", String, unique=True))
    fist_name: Optional[str]
    last_name: Optional[str]
