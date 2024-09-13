from pydantic import BaseModel
from typing import Any
from schemas.game.enums import MessageType, MessageReturnType

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
