from enum import Enum
from typing import Any
from pydantic import BaseModel


class TargetType(Enum):
    FIELD = "field"
    CARD = "card"
    PLAYER = "player"

class TargetFieldInfo(BaseModel):
    index: int
    player: int


class TargetInfo(BaseModel):
    type: TargetType
    data: int | TargetFieldInfo
