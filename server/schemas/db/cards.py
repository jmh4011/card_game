from pydantic import BaseModel

class CardBase(BaseModel):
    card_name: str
    card_class: str
    attack: int
    health: int
    image_path: str
    card_type: int

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class CardSchemas(CardBase):
    card_id: int
    effects: list[int] = []

    class Config:
        from_attributes = True
