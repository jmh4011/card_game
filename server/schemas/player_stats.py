from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone



class PlayerStatsBase(BaseModel):
    player_id: int
    current_deck_id: Optional[int] = None
    money: Optional[int] = 0

class PlayerStatsCreate(PlayerStatsBase):
    pass

class PlayerStatsUpdate(PlayerStatsBase):
    pass

class PlayerStats(PlayerStatsBase):
    stat_id: int
    last_updated: datetime

    class Config:
        from_attributes = True
