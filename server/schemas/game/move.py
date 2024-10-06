from pydantic import BaseModel
from schemas.game.enums import MoveType
from schemas.game.entity import Entity

class Move(BaseModel):
    move_type: MoveType
    entity: Entity
    select: bool
    targets: list[Entity]
    effect_id: int | None

class MoveReturn(BaseModel):
    move_index: int
    target: list[int]

    class Config:
        use_enum_values = True
