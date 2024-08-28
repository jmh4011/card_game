from pydantic import BaseModel, Field
from datetime import datetime, timezone
from schemas.cards import CardSchemas
from schemas.decks import DeckSchemas


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