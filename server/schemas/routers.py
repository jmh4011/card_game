from pydantic import BaseModel, Field
from datetime import datetime, timezone
from schemas.cards import CardSchemas
from schemas.decks import DeckSchemas


class RouterDeckUpdate(BaseModel):
    deck_name: str
    image_path: str
    deck_cards: dict[int,int]

class RouterDeckUpdateReturn(BaseModel):
    deck: DeckSchemas
    deck_cards: dict[int,int]


class RouterDeckCreate(BaseModel):
    deck_name: str
    image_path: str