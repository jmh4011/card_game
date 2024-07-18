
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone



class PlayerBase(BaseModel):
    username: str
    password: str

class PlayerCreate(PlayerBase):
    pass

class PlayerLogin(PlayerBase):
    pass

class Player(PlayerBase):
    refresh_token: str | None = None
    refresh_token_expiry: datetime | None = None
    player_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class PlayerUpdate(Player):
    pass
