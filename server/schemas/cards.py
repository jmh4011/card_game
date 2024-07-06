
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone



class CardBase(BaseModel):
    card_name: str
    card_class: Optional[str] = None
    attack: Optional[int] = None
    health: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None
    cost: Optional[int] = None
    card_type: Optional[int] = None

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class Card(CardBase):
    card_id: int

    class Config:
        from_attributes = True
