from sqlalchemy.ext.asyncio import AsyncSession
from crud import DeckCrud, UserCrud, DeckCardCrud
from schemas.cards import Card as CardSchemas
from services import DeckServices
import random

class Card:
    async def __init__(self, db: AsyncSession, card_id:int, card_info:CardSchemas) -> None:
        self.db = db
        self.card_id = card_id
        self.card_name = card_info.card_name
        self.card_class = card_info.card_class
        self.max_attack = card_info.attack
        self.attack = card_info.attack
        self.max_health = card_info.health
        self.health = card_info.health
        self.description = card_info.description
        self.card_type = card_info.card_type
        self.side_effect = []
    
    
        