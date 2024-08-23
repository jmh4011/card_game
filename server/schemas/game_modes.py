from pydantic import BaseModel

class GameModeBase(BaseModel):
    image_path: str
    description: str

class GameModeCreate(GameModeBase):
    pass

class GameModeUpdate(GameModeBase):
    pass

class GameModeSchemas(GameModeBase):
    mode_id: int

    class Config:
        from_attributes = True
