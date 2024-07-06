# server/services/decks.py
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import deck_crud
from ..schemas import decks as deck_schemas
from ..models import Deck

class deck_services:

    @staticmethod
    async def create_deck(db: AsyncSession, deck: deck_schemas.DeckCreate) -> Deck:
        return await deck_crud.create(db=db, deck=deck)

    @staticmethod
    async def get_deck(db: AsyncSession, player_id: int) -> list[Deck]:
        return await deck_crud.get(db=db, player_id=player_id)

    @staticmethod
    async def update_deck(db: AsyncSession, deck_id: int, deck: deck_schemas.DeckUpdate) -> Deck:
        return await deck_crud.update(db=db, deck_id=deck_id, deck=deck)

    @staticmethod
    async def delete_deck(db: AsyncSession, deck_id: int) -> Deck:
        return await deck_crud.delete(db=db, deck_id=deck_id)
