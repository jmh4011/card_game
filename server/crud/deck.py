# server/DB/crud/decks.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Deck, DeckCard
from schemas.decks import DeckCreate, DeckUpdate


class DeckCrud:

    @staticmethod
    async def get(db: AsyncSession, deck_id: int):
        result = await db.execute(select(Deck).filter(Deck.deck_id == deck_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, deck: DeckCreate):
        db_deck = Deck(**deck.model_dump())
        db.add(db_deck)
        return db_deck

    @staticmethod
    async def update(db: AsyncSession, deck_id: int, deck: DeckUpdate):
        db_deck = await db.get(Deck, deck_id)
        if db_deck:
            for key, value in deck.model_dump().items():
                setattr(db_deck, key, value)
            return db_deck
        return None

    @staticmethod
    async def delete(db: AsyncSession, deck_id: int):
        db_deck = await db.get(Deck, deck_id)
        if db_deck:
            await db.delete(db_deck)
            return db_deck
        return None

    @staticmethod
    async def get_all(db: AsyncSession, player_id: int):
        result = await db.execute(select(Deck).filter(Deck.player_id == player_id))
        return result.scalars().all()
    
    
    @staticmethod
    async def delete_all(db: AsyncSession, player_id: int):
        result = await db.execute(select(Deck).filter(Deck.player_id == player_id))
        db_decks = result.scalars().all()
        for deck in db_decks:
            await db.delete(deck)
        return db_decks