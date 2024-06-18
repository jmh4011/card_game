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
        

class DeckUpdate(Deck):
    pass


class DeckCardBase(BaseModel):
    deck_id: Optional[int] = None
    card_id: Optional[int] = None

class DeckCardCreate(DeckCardBase):
    pass

class DeckCard(DeckCardBase):
    deck_card_id: int

    class Config:
        from_attributes = True

class DeckCardUpdate(DeckCard):
    pass

class GameBase(BaseModel):
    player1_id: Optional[int] = None
    player2_id: Optional[int] = None
    winner_id: Optional[int] = None

class GameCreate(GameBase):
    pass

class Game(GameBase):
    game_id: int
    played_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True


class GameMoveBase(BaseModel):
    game_id: Optional[int] = None
    player_id: Optional[int] = None
    move_description: Optional[str] = None

class GameMoveCreate(GameMoveBase):
    pass

class GameMove(GameMoveBase):
    move_id: int
    move_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True


class PlayerStatsBase(BaseModel):
    player_id: int
    current_deck_id: Optional[int] = None
    money: int

class PlayerStatsCreate(PlayerStatsBase):
    pass

class PlayerStats(PlayerStatsBase):
    stat_id: int
    last_updated: datetime

    class Config:
        from_attributes = True