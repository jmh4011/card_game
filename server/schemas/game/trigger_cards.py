from pydantic import BaseModel
from modules.card import Card

class TriggerCards(BaseModel):
    summon: list[Card] = []
    effect: list[Card] = []
    draw: list[Card] = []
    move: list[Card] = []
    attack: list[Card] = []
    defence: list[Card] = []
    damage: list[Card] = []
    destroy: list[Card] = []

    class Config:
        arbitrary_types_allowed = True
