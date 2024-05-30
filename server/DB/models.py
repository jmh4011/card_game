# models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    cost = Column(Integer)
    attack = Column(Integer)
    health = Column(Integer)
    type = Column(String(50))
    text = Column(String(500))
    image = Column(String(250))

