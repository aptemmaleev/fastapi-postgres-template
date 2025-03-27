import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Request, APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from app.storage.postgres import async_session
from app.models import Session, User

from app.settings import SETTINGS
from app.utils.secrets import hash_password, verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


class AuthorizationError(Exception): ...


async def get_user_by_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        if SETTINGS.BRANCH != "main" and token == SETTINGS.API_TOKEN.get_secret_value():
            return User(role="ADMIN")
        async with async_session() as session:
            user_session = await Session.find_one(session, token=token, active=True)
            if not user_session:
                raise AuthorizationError
            user = await User.find_one(session, id=user_session.user_id)
            return user
    except AuthorizationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_admin_by_token(user: User = Depends(get_user_by_token)) -> User:
    if user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Forbidden")
    return user


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
):
    if (
        SETTINGS.BRANCH != "main"
        and form_data.username == SETTINGS.ADMIN_USERNAME.get_secret_value()
        and form_data.password == SETTINGS.ADMIN_PASSWORD.get_secret_value()
    ):
        return {
            "access_token": SETTINGS.API_TOKEN.get_secret_value(),
            "token_type": "bearer",
        }
    async with async_session() as session:
        user = await User.find_one(session, email=form_data.username)
        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
        if not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        user_session = Session(user_id=user.id)
        await user_session.save(session)

        return {
            "access_token": user_session.token,
            "token_type": "bearer",
        }
    raise HTTPException(status_code=400, detail="Incorrect username or password")


class AuthFormData(BaseModel):
    email: EmailStr
    password: str


@router.post("/users/create")
async def register(
    form_data: Annotated[AuthFormData, Depends()], request: Request
) -> User:
    async with async_session() as session:
        if await User.find_one(session, email=form_data.email):
            raise HTTPException(status_code=400, detail="Email already exists")
        user = User(email=form_data.email, password=hash_password(form_data.password))
        await user.save(session)
        return JSONResponse(
            status_code=201, content=user.model_dump(exclude={"password"})
        )


@router.get("/users/me")
async def who_am_i(user: User = Depends(get_user_by_token)):
    return JSONResponse(status_code=200, content=user.model_dump(exclude={"password"}))


@router.get("/users")
async def list_users(
    user: User = Depends(get_admin_by_token), limit: int = 10, offset: int = 0
):
    async with async_session() as session:
        users = await User.find_many(session=session, limit=limit, offset=offset)
        return JSONResponse(
            status_code=200,
            content=[user.model_dump(exclude={"password"}) for user in users],
        )


@router.delete("/users/{user_id}")
async def delete_user(user_id: uuid.UUID, user: User = Depends(get_admin_by_token)):
    async with async_session() as session:
        user = await User.find_one(session, id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await User.delete(session, id=user_id)
        return JSONResponse(status_code=200, content={"message": "User deleted"})
