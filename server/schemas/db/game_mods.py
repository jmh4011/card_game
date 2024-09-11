from pydantic import BaseModel

class GameModBase(BaseModel):
    mod_name: str
    image_path: str
    description: str
    is_open: bool

class GameModCreate(GameModBase):
    pass

class GameModUpdate(GameModBase):
    pass

class GameModSchemas(GameModBase):
    mod_id: int

    class Config:
        from_attributes = True
