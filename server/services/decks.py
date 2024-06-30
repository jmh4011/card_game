# server/services/decks.py
from sqlalchemy.ext.asyncio import AsyncSession
from ..DB.crud import decks as crud_decks
from ..DB.schemas import DeckCreate, DeckUpdate
from ..DB.models import Deck

async def create_deck(db: AsyncSession, deck: DeckCreate) -> Deck:
    return await crud_decks.create_deck(db=db, deck=deck)

async def get_deck(db: AsyncSession, player_id: int) -> list[Deck]:
    return await crud_decks.get_deck(db=db, player_id=player_id)

async def update_deck(db: AsyncSession, deck_id: int, deck: DeckUpdate) -> Deck:
    return await crud_decks.update_deck(db=db, deck_id=deck_id, deck=deck)

async def delete_deck(db: AsyncSession, deck_id: int) -> Deck:
    return await crud_decks.delete_deck(db=db, deck_id=deck_id)
