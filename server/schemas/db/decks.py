from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone



class DeckBase(BaseModel):
    deck_name: str
    image_path: str
    is_public: bool = False

class DeckCreate(DeckBase):
    user_id: int

class DeckUpdate(DeckBase):
    pass

class DeckSchemas(DeckBase):
    user_id: int
    deck_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True