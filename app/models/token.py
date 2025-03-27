import uuid

from sqlalchemy import Column, String
from sqlmodel import Field
from datetime import datetime, timedelta

from app.storage.base_types import BaseModel
from app.utils.secrets import create_token

# fmt: off

class Session(BaseModel, table=True):
    __tablename__ = "sessions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")

    token: str = Field(default_factory=create_token, sa_column=Column(String, nullable=False))
    active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=30))

# fmt: on
