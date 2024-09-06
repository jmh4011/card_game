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

class DeckRetrun(BaseModel):
    pass

class DeckSchemas(DeckBase):
    user_id: int
    deck_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True



class RouterDeckUpdate(BaseModel):
    deck_name: str
    image_path: str
    deck_cards: dict[int,int]
    is_public: bool

class RouterDeckUpdateReturn(BaseModel):
    deck: DeckSchemas
    deck_cards: dict[int,int]

class RouterDeckGetReturn(BaseModel):
    deck: DeckSchemas
    deck_cards: dict[int,int]
    read_only: bool

class RouterDeckCreate(BaseModel):
    deck_name: str
    image_path: str