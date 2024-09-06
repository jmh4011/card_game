from pydantic import BaseModel


class EffectBase(BaseModel):
    effect_name: str
    description: str

class EffectCreate(EffectBase):
    pass

class EffectUpdate(EffectBase):
    pass

class EffectSchemas(EffectBase):
    effect_id: int

    class Config:
        from_attributes = True