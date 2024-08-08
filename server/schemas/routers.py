from pydantic import BaseModel, Field
from datetime import datetime, timezone
from schemas.cards import Card
from schemas.decks import Deck


class RouterDeckUpdate(BaseModel):
    deck_name: str
    image_path: str
    deck_cards: dict[int,int]

class RouterDeckUpdateReturn(BaseModel):
    deck: Deck
    deck_cards: dict[int,int]


class RouterDeckCreate(BaseModel):
    deck_name: str
    image_path: str

class RouterDeckCard(Card):
    deck_card_count: int
    player_card_count: int