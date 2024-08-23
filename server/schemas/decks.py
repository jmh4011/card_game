from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone



class DeckBase(BaseModel):
    user_id: int
    deck_name: str
    image_path: str

class DeckCreate(DeckBase):
    pass

class DeckUpdate(DeckBase):
    pass

class DeckSchemas(DeckBase):
    deck_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
