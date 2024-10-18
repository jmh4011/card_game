from enum import Enum
from pydantic import BaseModel

class EntityType(Enum):
    HAND = "hand"
    FIELD = "field"
    GRAVE = "grave"
    DECK = "deck"
    PLAYER = "player"
    

class Entity(BaseModel):
    index: int | None
    opponent: bool
    type: EntityType

    class Config:
        use_enum_values = True
