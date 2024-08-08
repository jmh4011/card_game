from pydantic import BaseModel
from datetime import datetime



class UserStatBase(BaseModel):
    user_id: int
    money: int = 0
    nickname: str

class UserStatCreate(UserStatBase):
    pass

class UserStatUpdate(UserStatBase):
    pass

class UserStat(UserStatBase):
    stat_id: int
    last_updated: datetime

    class Config:
        from_attributes = True
