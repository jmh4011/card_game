
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone



class PlayerBase(BaseModel):
    username: str
    password: str
    refresh_token: Optional[str] = None
    refresh_token_expiry: Optional[datetime] = None

class PlayerCreate(PlayerBase):
    pass

class PlayerLogin(PlayerBase):
    pass

class Player(PlayerBase):
    player_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class PlayerUpdate(Player):
    pass
