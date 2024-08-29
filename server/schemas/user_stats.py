from pydantic import BaseModel
from datetime import datetime



class UserStatBase(BaseModel):
    money: int = 0
    nickname: str
    current_mod_id: int = 1

class UserStatCreate(UserStatBase):
    user_id: int

class UserStatUpdate(UserStatBase):
    pass

class UserStatSchemas(UserStatBase):
    stat_id: int
    last_updated: datetime

    class Config:
        from_attributes = True
