# schemas.py
from pydantic import BaseModel

class UserBase(BaseModel):
    userid: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    name: str

    class Config:
        orm_mode = True

class CardBase(BaseModel):
    name: str
    cost: int
    attack: int
    health: int
    type: str
    text: str
    image: str

class CardCreate(CardBase):
    pass

class Card(CardBase):
    id: int

    class Config:
        orm_mode = True

