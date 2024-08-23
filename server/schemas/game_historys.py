from pydantic import BaseModel, Field
from datetime import datetime, timezone

class GameHistoryBase(BaseModel):
    user1_id: int
    user2_id: int
    winner_id: int

class GameHistoryCreate(GameHistoryBase):
    pass

class GameHistoryUpdate(GameHistoryBase):
    pass

class GameHistorySchemas(GameHistoryBase):
    deck_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
