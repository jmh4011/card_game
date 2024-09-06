from pydantic import BaseModel




class CardEffectBase(BaseModel):
    card_id: int
    effect_id: int

class CardEffectCreate(CardEffectBase):
    pass

class CardEffectUpdate(CardEffectBase):
    pass

class CardEffectSchemas(CardEffectBase):
    card_effect_id: int

    class Config:
        from_attributes = True