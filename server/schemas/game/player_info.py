from pydantic import BaseModel
from schemas.game.card_info import CardInfo

class PlayerInfo(BaseModel):
    cost: int
    health: int
    side_effects: list[int] = []
    hands: list[CardInfo]
    fields: dict[int, CardInfo] = {}
    graves: list[CardInfo]
    decks: int
