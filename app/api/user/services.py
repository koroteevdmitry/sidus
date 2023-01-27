from uuid import UUID

from fastapi.params import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.user.schemas import UserCreateSchema, UserUpdateSchema
from db.db import db_session
from db.models.user import User


class UserService:
    def __init__(self, session: AsyncSession = Depends(db_session)):
        self.session = session

    async def get_user_by_id(self, uid: UUID) -> User:
        return await self.session.get(User, uid)

    async def get_user_by_email(self, email: str) -> User:
        user = await self.session.execute(select(User).where(User.email == email))
        return user.scalars().first()

    async def get_user_by_username(self, username: str) -> User:
        user = await self.session.execute(select(User).where(User.username == username))
        return user.scalars().first()

    async def create_and_return_user(self, data: UserCreateSchema) -> User:
        user = User(**data.dict())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_and_return_user(self, uid: UUID, data: UserUpdateSchema) -> User:
        user = await self.get_user_by_id(uid)
        await self.session.execute(update(User).where(User.id == uid).values(**data.dict(exclude_unset=True)))
        await self.session.commit()
        await self.session.refresh(user)
        return user
