from sqlalchemy.ext.asyncio import AsyncSession
from crud import card_crud,deck_card_crud,player_card_crud
from schemas.cards import Card
from schemas.routers import RouterDeckCard
from utils import handle_transaction, to_dict

class card_services:
    @staticmethod
    async def get(db:AsyncSession) -> dict[int,Card]:
        cards = await card_crud.get_all(db=db)
        return {card.card_id:card for card in cards}
