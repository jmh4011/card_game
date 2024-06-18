from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import DeckCard
from ..schemas import DeckCard, DeckCardCreate, DeckCardUpdate
from fastapi import Depends

async def get_deck_cards(db: AsyncSession, deck_id: int):
    result = await db.execute(select(DeckCard).filter(DeckCard.deck_id == deck_id))
    return result.scalars().all()

async def create_deck_cards(db: AsyncSession, deck_id: int, cards_id: list[int]):
    async with db.begin():
        db.add_all(
            [DeckCard(deck_id=deck_id, card_id=card_id) for card_id in cards_id]
        )
    await db.commit()

async def delete_deck_cards(db: AsyncSession, deck_id: int):
    async with db.begin():
        await db.execute(select(DeckCard).filter(DeckCard.deck_id == deck_id).delete())
    await db.commit()
