from typing import Annotated

from fastapi import Depends, HTTPException, Request, APIRouter, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.settings import SETTINGS


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


async def check_token(token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    if token == SETTINGS.API_TOKEN.get_secret_value():
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
):
    if (
        form_data.username == SETTINGS.ADMIN_USERNAME.get_secret_value()
        and form_data.password == SETTINGS.ADMIN_PASSWORD.get_secret_value()
    ):
        return {
            "access_token": SETTINGS.API_TOKEN.get_secret_value(),
            "token_type": "bearer",
        }
    raise HTTPException(status_code=400, detail="Incorrect username or password")
