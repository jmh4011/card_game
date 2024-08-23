from pydantic import BaseModel, Field
from datetime import datetime, timezone

class GameHistoryMoveBase(BaseModel):
    game_id: int
    user_id: int
    move_description: int

class GameHistoryMoveCreate(GameHistoryMoveBase):
    pass 

class GameHistoryMoveUpdate(GameHistoryMoveBase):
    pass



class GameHistoryMoveSchemas(GameHistoryMoveBase):
    move_id: int
    move_timestamp : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
