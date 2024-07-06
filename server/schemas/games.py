from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone


class GameBase(BaseModel):
    player1_id = Optional[int] = None
    player2_id = Optional[int] = None
    winner_id = Optional[int] = None

class GameCreate(GameBase):
    pass

class GameUpdate(GameBase):
    pass

class Game(GameBase):
    deck_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True