
from pydantic import BaseModel
from schemas.db.effects import EffectSchemas
from schemas.db.cards import CardSchemas


class CardRetrun(BaseModel):
    cards: dict[int, CardSchemas] 
    effects: dict[int, EffectSchemas]