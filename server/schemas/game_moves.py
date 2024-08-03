from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class GameMoveBase(BaseModel):
    game_id: int
    user_id: int
    move_description: int

class GameMoveCreate(GameMoveBase):
    pass 

class GameMoveUpdate(GameMoveBase):
    pass



class GameMove(GameMoveBase):
    move_id: int
    move_timestamp : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
