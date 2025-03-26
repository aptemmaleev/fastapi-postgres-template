from fastapi import APIRouter
from starlette.responses import JSONResponse


router = APIRouter()


@router.get("/")
async def root():
    return JSONResponse(status_code=200, content={"message": "Bober Rostislav"})
