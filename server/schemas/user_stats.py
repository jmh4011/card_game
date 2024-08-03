from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone



class UserStatsBase(BaseModel):
    user_id: int
    money: int = 0
    nickname: str

class UserStatsCreate(UserStatsBase):
    pass

class UserStatsUpdate(UserStatsBase):
    pass

class UserStats(UserStatsBase):
    stat_id: int
    last_updated: datetime

    class Config:
        from_attributes = True
