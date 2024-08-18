
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone



class CardBase(BaseModel):
    card_name: str
    card_class: str
    attack: int
    health: int
    description: str
    image_path: str
    card_type: int

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class Card(CardBase):
    card_id: int

    class Config:
        from_attributes = True
