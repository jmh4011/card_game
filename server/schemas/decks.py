from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone



class DeckBase(BaseModel):
    player_id: Optional[int] = None
    deck_name: Optional[str] = None
    image: Optional[str] = None

class DeckCreate(DeckBase):
    pass

class DeckUpdate(DeckBase):
    pass

class Deck(DeckBase):
    deck_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
