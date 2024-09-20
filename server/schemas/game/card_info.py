from schemas.db.cards import CardSchemas
from schemas.game.enums import ZoneType
from pydantic import BaseModel

class CardInfo(CardSchemas):
    side_effects: list[int] = []

    class Config:
        use_enum_values = True
