from pydantic import BaseModel

class GameModeBase(BaseModel):
    image_path: str
    description: str

class GameModeCreate(GameModeBase):
    pass

class GameModeUpdate(GameModeBase):
    pass

class GameMode(GameModeBase):
    mode_id: int

    class Config:
        from_attributes = True
