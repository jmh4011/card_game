from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from server.schemas import cards as cards_shemas

class PlayerCardBase(BaseModel):
    player_id:int
    card_id:int

class PlayerCardCreate(PlayerCardBase):
    pass

class PlayerCardUpdate(PlayerCardBase):
    pass

class PlayerCard(PlayerCardBase):
    player_card_id : int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class PlayerCardReturn(cards_shemas.Card):
    card_count: int
