from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from core.utils import get_hashed_password


class UserSchema(BaseModel):
    id: UUID
    username: str
    email: str
    fist_name: str
    last_name: Optional[str]


class UserCreateSchema(BaseModel):
    username: str
    email: str
    fist_name: Optional[str]
    last_name: Optional[str]
    password: str

    @classmethod
    def create(cls, **data):
        data['password'] = get_hashed_password(data['password'])
        return cls.parse_obj(data)


class UserUpdateSchema(BaseModel):
    email: Optional[str]
    fist_name: Optional[str]
    last_name: Optional[str]

    @classmethod
    def create(cls, **data):
        return cls.parse_obj(data)
