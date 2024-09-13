from pydantic import BaseModel
from schemas.game.enums import EntityZoneType

class Entity(BaseModel):
    zone: EntityZoneType
    index: int
    opponent: bool

    class Config:
        use_enum_values = True
