from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class DeckCardBase(BaseModel):
    deck_id: int
    card_id: int
    card_count: int

class DeckCardCreate(DeckCardBase):
    pass

class DeckCardUpdate(DeckCardBase):
    pass

class DeckCard(DeckCardBase):
    deck_card_id: int

    class Config:
        from_attributes = True
