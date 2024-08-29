from pydantic import BaseModel

from pydantic import BaseModel, Field
from datetime import datetime, timezone

class UserDeckSelectionBase(BaseModel):
    user_id: int
    mod_id: int
    deck_id: int

class UserDeckSelectionCreate(UserDeckSelectionBase):
    pass

class UserDeckSelectionUpdate(BaseModel):
    game_mode: str |None = None
    deck_id: str | None = None

class UserDeckSelectionSchemas(UserDeckSelectionBase):
    selection_id: int
    selection_date: datetime  = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
