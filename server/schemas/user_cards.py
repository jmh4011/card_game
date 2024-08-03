from pydantic import BaseModel, Field
from datetime import datetime, timezone
from schemas import cards as cards_shemas

class UserCardBase(BaseModel):
    user_id:int
    card_id:int

class UserCardCreate(UserCardBase):
    pass

class UserCardUpdate(UserCardBase):
    pass

class UserCard(UserCardBase):
    user_card_id : int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class UserCardReturn(cards_shemas.Card):
    card_count: int
