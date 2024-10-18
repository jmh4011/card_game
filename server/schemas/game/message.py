from enum import Enum
from pydantic import BaseModel
from typing import Any

class MessageType(Enum):
    PING = "ping"
    TEXT = "text"
    GAME_INFO = "game_info"
    ACRION = "action"
    MOVE = "move"

class MessageReturnType(Enum):
    TEXT = "text"
    MOVE = "move"
    CANCEL = "cancel"
    END = "end"

class MessageModel(BaseModel):
    type: MessageType
    data: Any

    class Config:
        use_enum_values = True


class MessageReturnModel(BaseModel):
    type: MessageReturnType
    data: Any

    class Config:
        use_enum_values = True
