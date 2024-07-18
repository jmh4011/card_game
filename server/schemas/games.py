from pydantic import BaseModel, Field
from datetime import datetime, timezone

class GameBase(BaseModel):
    player1_id: int
    player2_id: int
    winner_id: int

class GameCreate(GameBase):
    pass

class GameUpdate(GameBase):
    pass

class Game(GameBase):
    deck_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
