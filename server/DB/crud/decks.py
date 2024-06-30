# server/DB/crud/decks.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import Deck, DeckCard
from ..schemas import DeckCreate, DeckUpdate

async def get_deck(db: AsyncSession, player_id: int):
    result = await db.execute(select(Deck).filter(Deck.player_id == player_id))
    return result.scalars().all()

async def create_deck(db: AsyncSession, deck: DeckCreate):
    db_deck = Deck(**deck.model_dump())
    db.add(db_deck)
    return db_deck

async def update_deck(db: AsyncSession, deck_id: int, deck: DeckUpdate):
    db_deck = await db.get(Deck, deck_id)
    if db_deck:
        db_deck.deck_name = deck.deck_name
        db_deck.image = deck.image
        return db_deck
    return None

async def delete_deck(db: AsyncSession, deck_id: int):
    db_deck = await db.get(Deck, deck_id)
    if db_deck:
        await db.delete(db_deck)
        return db_deck
    return None
