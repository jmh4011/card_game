from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import Deck
from ..schemas import DeckCard, DeckCreate, DeckUpdate

async def get_deck(db: AsyncSession, player_id: int):
    result = await db.execute(select(Deck).filter(Deck.player_id == player_id))
    return result.scalars().all()

async def create_deck(db: AsyncSession, deck: DeckCreate):
    db_deck = Deck(**deck.model_dump())
    db.add(db_deck)
    await db.commit()
    await db.refresh(db_deck)
    return db_deck

async def update_deck(db: AsyncSession, deck_id: int, deck: DeckUpdate):
    db_deck = await db.get(Deck, deck_id)
    if db_deck:
        for key, value in deck.model_dump().items():
            setattr(db_deck, key, value)
        await db.commit()
        await db.refresh(db_deck)
        return db_deck
    return None

async def delete_deck(db: AsyncSession, deck_id: int):
    db_deck = await db.get(Deck, deck_id)
    if db_deck:
        await db.delete(db_deck)
        await db.commit()
        return db_deck
    return None
