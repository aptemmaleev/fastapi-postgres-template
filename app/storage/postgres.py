import json
import logging

from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.settings import SETTINGS

engine = create_async_engine(SETTINGS.POSTGRES_URL.get_secret_value(), echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Register default JSON encoder for support ObjectId
default_encoder = json.JSONEncoder.default


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return default_encoder(self, o)


json.JSONEncoder.default = JSONEncoder().default
