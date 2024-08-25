from pydantic import BaseModel

class GameModBase(BaseModel):
    image_path: str
    description: str

class GameModCreate(GameModBase):
    pass

class GameModUpdate(GameModBase):
    pass

class GameModSchemas(GameModBase):
    mod_id: int

    class Config:
        from_attributes = True
