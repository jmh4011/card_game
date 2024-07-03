# server/DB/schemas.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

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

class Card(CardBase):
    card_id: int

    class Config:
        from_attributes = True

class PlayerBase(BaseModel):
    username: str
    password: str

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    player_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class PlayerUpdate(Player):
    pass

class DeckBase(BaseModel):
    player_id: Optional[int] = None
    deck_name: Optional[str] = None
    image: Optional[str] = None

class DeckCreate(DeckBase):
    pass

class Deck(DeckBase):
    deck_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class DeckCardBase(BaseModel):
    deck_id: Optional[int] = None
    card_id: Optional[int] = None

class DeckCardCreate(DeckCardBase):
    pass

class DeckCard(DeckCardBase):
    deck_card_id: int

    class Config:
        from_attributes = True

class DeckUpdate(BaseModel):
    deck_name: str
    image: str
    deck_cards: list[int]

class PlayerStatsBase(BaseModel):
    player_id: int
    current_deck_id: Optional[int] = None
    money: Optional[int] = 0

class PlayerStatsCreate(PlayerStatsBase):
    pass

class PlayerStats(PlayerStatsBase):
    stat_id: int
    last_updated: datetime

    class Config:
        from_attributes = True

class PlayerCardBase(BaseModel):
    player_id:int
    card_id:int

class PlayerCardCreate(PlayerCardBase):
    pass

class PlayerCard(PlayerCardBase):
    player_card_id : int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class PlayerCardReturn(Card):
    card_count: int

class DeckUpdateReturn(BaseModel):
    deck: Deck
    deck_cards: list[PlayerCardReturn]
