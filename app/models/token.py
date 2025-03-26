import uuid

from sqlmodel import Field
from datetime import datetime

from app.storage.base_types import BaseModel

# fmt: off

class Token(BaseModel, table=True):
    __tablename__ = "tokens"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")

    active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime = Field(default_factory=datetime.now)

# fmt: on
