import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import (
    request_validation_exception_handler,
    http_exception_handler,
)
from starlette.responses import JSONResponse

from app.settings import SETTINGS
from app.logger import setup as setup_logger

from .routes import main_router


app = FastAPI(
    title=f"Service {SETTINGS.BRANCH}",
    description="Сервис заготовка FastApi + SQLModel",
)
# NOTE: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)


@app.on_event("startup")
async def app_startup():
    os.system("clear")
    setup_logger()
    logging.info("Server started")


# Error handling
def log_fastapi_error(exc: Exception):
    logging.error(f"[CORE]: {exc.__class__.__name__} in FastAPI: {exc}")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    log_fastapi_error(exc)
    return await request_validation_exception_handler(request, exc)


@app.exception_handler(HTTPException)
async def handler(request: Request, exc: HTTPException):
    log_fastapi_error(exc)
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def any_exception_handler(request: Request, exc: Exception):
    log_fastapi_error(exc)
    return JSONResponse(
        status_code=500, content={"message": "Something went wrong: " + str(exc)}
    )
