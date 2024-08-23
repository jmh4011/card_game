from sqlalchemy.ext.asyncio import AsyncSession
from crud import CardCrud
from schemas.cards import CardSchemas

class CardServices:
    @staticmethod
    async def get(db: AsyncSession) -> dict[int, CardSchemas]:
        cards = await CardCrud.get_all(db=db)
        return {card.card_id: card for card in cards}
