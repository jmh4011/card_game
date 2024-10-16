from enum import Enum
from pydantic import BaseModel

class EntityType(Enum):
    FIELD = "field"
    PLAYER = "player"
    CARD = "card"

class Entity(BaseModel):
    id: int
    zone: EntityType

    class Config:
        use_enum_values = True
