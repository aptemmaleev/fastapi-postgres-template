from os import environ
from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr

load_dotenv(".env")


class Settings(BaseModel):
    LOGGING_LEVEL: str
    BRANCH: str

    API_TOKEN: SecretStr
    API_PORT: int
    API_HOST: str
    ADMIN_USERNAME: SecretStr
    ADMIN_PASSWORD: SecretStr

    POSTGRES_URL: SecretStr


SETTINGS = Settings(**environ)
