from sqlalchemy.ext.asyncio import AsyncSession
from crud import DeckCardCrud,DeckCrud
from schemas.decks import DeckUpdate, DeckCreate
from schemas.routers import RouterDeckUpdate, RouterDeckUpdateReturn, RouterDeckCreate, RouterDeckCard
from models import Deck
from utils import handle_transaction, to_dict
import logging

logger = logging.getLogger(__name__)

class DeckServices:

    @staticmethod
    async def get(db: AsyncSession, user_id: int) -> Deck:
        decks = await handle_transaction(db=db, func=DeckCrud.get_all, user_id=user_id)
        for deck in decks:
            await db.refresh(deck)
        return decks
    
    @staticmethod
    async def update(db: AsyncSession, user_id:int, deck_id: int, deck: RouterDeckUpdate) -> RouterDeckUpdateReturn:
        logger.info(f"\n\n{deck.deck_cards}\n\n")
        db_deck = await handle_transaction(db=db, func=DeckCrud.get,should_refresh=True, deck_id=deck_id)

        if db_deck is None or db_deck.user_id != user_id:
            return None
        result_deck = await handle_transaction(db=db, func=DeckCrud.update, should_refresh=True,deck_id=deck_id, deck=DeckUpdate(user_id=user_id,deck_name=deck.deck_name, image=deck.image))
        if result_deck is None:
            return None
    

        result_cards = await handle_transaction(db, DeckCardCrud.update_all, deck_id, cards=deck.deck_cards)
        for result_card in result_cards:
            await db.refresh(result_card)
        await db.refresh(result_deck)
        return RouterDeckUpdateReturn(deck= result_deck, deck_cards={card.card_id: card.card_count for card in result_cards})
    
    @staticmethod
    async def create(db: AsyncSession, user_id:int, deck:RouterDeckCreate):
        deck_data = DeckCreate(user_id=user_id, deck_name=deck.deck_name, image=deck.image)
        deck = await handle_transaction(db, DeckCrud.create, should_refresh=True, deck=deck_data)
        return deck
    
    
    @staticmethod
    async def get_cards(db: AsyncSession, deck_id: int) -> dict[int,int]:
        deck_cards = await handle_transaction(db=db, func=DeckCardCrud.get_all, deck_id=deck_id)
        for card in deck_cards:
            await db.refresh(card)
        return {deck_card.card_id:deck_card.card_count for deck_card in deck_cards}