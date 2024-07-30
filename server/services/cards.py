from sqlalchemy.ext.asyncio import AsyncSession
from crud import CardCrud
from schemas.cards import Card
from schemas.routers import RouterDeckCard
from utils import handle_transaction, to_dict

class CardServices:
    @staticmethod
    async def get(db:AsyncSession) -> dict[int,Card]:
        cards = await CardCrud.get_all(db=db)
        return {card.card_id:card for card in cards}
