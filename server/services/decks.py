# server/services/decks.py
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import deck_crud, deck_card_crud
from ..schemas.decks import DeckUpdate
from ..schemas.routers import RouterDeckUpdate
from ..models import Deck

class deck_services:

    @staticmethod
    async def get(db: AsyncSession, player_id: int) -> Deck:
        return await deck_crud.get_all(db=db, player_id=player_id)
    
    
    @staticmethod
    async def update(db: AsyncSession, deck_id: int, deck: RouterDeckUpdate):
        result_deck = await deck_crud.update(db=db, deck_id=deck_id, deck=DeckUpdate(deck_name=deck.deck_name, image=deck.image))
        if result_deck is None:
            return None
        result_cards = await deck_card_crud.update_all(db=db, deck_id=deck_id, deck_cards_id=deck.deck_cards)
    