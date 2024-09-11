from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone



class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    refresh_token: str | None = None
    refresh_token_expiry: datetime | None = None

class UserSchemas(UserBase):
    refresh_token: str | None = None
    refresh_token_expiry: datetime | None = None
    user_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True


