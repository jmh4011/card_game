from schemas.db.cards import CardSchemas
from schemas.game.enums import ZoneType
from pydantic import BaseModel

class CardInfo(CardSchemas):
    max_health: int
    side_effects: list[int] = []

    class Config:
        use_enum_values = True

class PlayerInfo(BaseModel):
    cost: int
    health: int
    attack: int
    effects: list[int] = []
    side_effects: list[int] = []
    hands: list[CardInfo] = []
    fields: dict[int, CardInfo] = {}
    graves: list[CardInfo] = []
    decks: int
    

class GameInfo(BaseModel):
    player: PlayerInfo
    opponent: PlayerInfo
    turn: int
    is_player_turn: bool
    effects: list[int] = []
    side_effects: list[int] = []

    class Config:
        use_enum_values = True
