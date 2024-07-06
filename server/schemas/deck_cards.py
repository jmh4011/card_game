from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class DeckCardBase(BaseModel):
    deck_id: Optional[int] = None
    card_id: Optional[int] = None

class DeckCardCreate(DeckCardBase):
    pass

class DeckCardUpdate(DeckCardBase):
    pass

class DeckCard(DeckCardBase):
    deck_card_id: int

    class Config:
        from_attributes = True
