from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class GameMoveBase(BaseModel):
    game_id = Optional[int] = None
    player_id = Optional[int] = None
    move_description = Optional[str] = None

class GameMoveCreate(GameMoveBase):
    pass 

class GameMoveUpdate(GameMoveBase):
    pass



class GameMove(GameMoveBase):
    move_id = player_id = Optional[int] = None
    move_timestamp = datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
