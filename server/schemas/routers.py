from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone


class RouterDeckUpdate(BaseModel):
    deck_name: Optional[str] = None
    image: Optional[str] = None
    deck_cards: Optional[list[int]] = None