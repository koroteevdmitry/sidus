from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.user.schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from api.user.services import UserService
from db.models.user import User

router = APIRouter()


class CreateUserRequestPayload(BaseModel):
    username: str
    password: str
    email: str
    fist_name: Optional[str]
    last_name: Optional[str]


class UpdateUserRequestPayload(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]
    fist_name: Optional[str]
    last_name: Optional[str]


@router.get("/uid/", response_model=UserSchema)
async def get_user(uid: UUID, service: UserService = Depends()) -> User:
    if not (user := await service.get_user_by_id(uid)):
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='No such user found.')
    return user


@router.post("/", response_model=UserSchema)
async def create_user(payload: CreateUserRequestPayload, service: UserService = Depends()) -> User:
    if await service.get_user_by_email(payload.email):
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='User with this email already exists.')
    if await service.get_user_by_username(payload.username):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='User with this username already exists.'
        )

    return await service.create_and_return_user(UserCreateSchema.create(**payload.dict()))


@router.put("/uid/", response_model=UserSchema)
async def update_user(uid: UUID, payload: UpdateUserRequestPayload, service: UserService = Depends()) -> User:
    if payload.dict(exclude_unset=True) is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Empty payload.')
    if not (user := await service.get_user_by_id(uid)):
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='No such user found.')
    if await service.get_user_by_email(payload.email) and user.email != payload.email:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='User with this email already exists.')
    if await service.get_user_by_username(payload.username) and user.username != payload.username:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='User with this username already exists.'
        )
    return await service.update_and_return_user(uid, UserUpdateSchema.create(**payload.dict(exclude_unset=True)))