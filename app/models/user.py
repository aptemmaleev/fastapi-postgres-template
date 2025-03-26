from typing import Optional
import uuid

from sqlmodel import Field
from datetime import datetime
from sqlalchemy import Column, Enum, String

from app.storage.base_types import BaseModel
from .enums import UserRole

# fmt: off

class User(BaseModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    role: UserRole = Field(sa_column=Column(String, nullable=False))

    service_name: Optional[str] = Field(default=None, sa_column=Column(String))

    email: Optional[str] = Field(default=None, sa_column=Column(String))
    password: Optional[str] = Field(default=None, sa_column=Column(String))
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# fmt: on
