from http import HTTPStatus
from typing import Optional
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from api.user.schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from api.user.services import UserService
from core.di.container import Container
from core.redis import AsyncRedis
from core.utils import verify_password
from db.models.user import User

router = APIRouter()


class CreateUserRequestPayload(BaseModel):
    username: str
    password: str
    email: str
    fist_name: Optional[str]
    last_name: Optional[str]


class UpdateUserRequestPayload(BaseModel):
    password: Optional[str]
    email: Optional[str]
    fist_name: Optional[str]
    last_name: Optional[str]


@router.get('/uid/', response_model=UserSchema)
@inject
async def get_user(
    uid: UUID,
    redis: AsyncRedis = Depends(Provide[Container.redis_service]),
    service: UserService = Depends(),
) -> User:
    if not (user := await service.get_user_by_id(uid)):
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='No such user found.')
    if not (value := await redis.get(str(uid), dict_value=True)):
        await redis.set(str(uid), user.dict())
        return user
    else:
        return User.parse_obj(value)


@router.post('/', response_model=UserSchema)
async def create_user(payload: CreateUserRequestPayload, service: UserService = Depends()) -> User:
    if await service.get_user_by_email(payload.email):
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='User with this email already exists.')
    if await service.get_user_by_username(payload.username):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='User with this username already exists.'
        )

    return await service.create_and_return_user(UserCreateSchema.create(**payload.dict()))


async def _authentication(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(), ) -> User:
    if not (user := await service.get_user_by_username(form_data.username)):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Incorrect username or password."
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Incorrect username or password."
        )
    return user


@router.put('/uid/', response_model=UserSchema)
@inject
async def update_user(
    uid: UUID,
    email: Optional[str] = Form(None),
    fist_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    service: UserService = Depends(),
    auth_user: User = Depends(_authentication),
    redis: AsyncRedis = Depends(Provide[Container.redis_service]),
) -> User:
    payload = UpdateUserRequestPayload(
        email=email,
        fist_name=fist_name,
        last_name=last_name,
    )
    if not payload.dict(exclude_none=True):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Empty payload.')
    if await service.get_user_by_email(payload.email) and auth_user.email != payload.email:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='User with this email already exists.')

    await redis.delete(str(uid))
    return await service.update_and_return_user(uid, UserUpdateSchema.create(**payload.dict(exclude_none=True)))
