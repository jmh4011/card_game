from pydantic import BaseModel
from schemas.db.decks import DeckSchemas


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