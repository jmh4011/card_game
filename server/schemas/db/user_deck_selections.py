from pydantic import BaseModel

from pydantic import BaseModel, Field
from datetime import datetime, timezone

class UserDeckSelectionBase(BaseModel):
    mod_id: int
    deck_id: int

class UserDeckSelectionCreate(UserDeckSelectionBase):
    user_id: int

class UserDeckSelectionUpdate(UserDeckSelectionBase):
    pass

class UserDeckSelectionSchemas(UserDeckSelectionBase):
    user_id: int
    selection_id: int
    selection_date: datetime  = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
