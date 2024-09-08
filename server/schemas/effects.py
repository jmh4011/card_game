from pydantic import BaseModel


class EffectBase(BaseModel):
    effect_name: str
    condition: str | None
    cost: str | None
    effect: str | None 

class EffectCreate(EffectBase):
    pass

class EffectUpdate(EffectBase):
    pass

class EffectSchemas(EffectBase):
    effect_id: int

    class Config:
        from_attributes = True