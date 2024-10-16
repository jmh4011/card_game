from pydantic import BaseModel, ConfigDict

class TriggerCards(BaseModel):
    summon: list[int] = []
    effect: list[int] = []
    draw: list[int] = []
    move: list[int] = []
    attack: list[int] = []
    defence: list[int] = []
    damage: list[int] = []
    destroy: list[int] = []
