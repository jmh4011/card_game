from sqlalchemy.ext.asyncio import AsyncSession
from crud import DeckCardCrud,DeckCrud
from schemas.db.decks import DeckUpdate, DeckCreate
from schemas.router.decks import RouterDeckGetReturn, RouterDeckUpdate, RouterDeckUpdateReturn, RouterDeckCreate
from models import Deck, DeckCard
import logging

logger = logging.getLogger(__name__)

class DeckServices:

    @staticmethod
    async def get_all(db: AsyncSession, user_id: int) -> Deck:
        decks = await DeckCrud.get_all(db=db, user_id=user_id)
        for deck in decks:
            await db.refresh(deck)
        return decks
    
    @staticmethod
    async def get(db: AsyncSession, user_id: int, deck_id: int) -> RouterDeckGetReturn | None:
        deck: Deck = await DeckCrud.get(db=db, deck_id=deck_id)
        if not deck: 
            return None
        await db.refresh(deck)
        if deck.user_id != user_id and not deck.is_public:
            return None
        deck_cards: list[DeckCard] = await DeckCardCrud.get_all(db=db, deck_id=deck_id)
        for card in deck_cards:
            await db.refresh(card)
        deck_cards = {deck_card.card_id:deck_card.card_count for deck_card in deck_cards}
        await db.refresh(deck)
        read_only = deck.user_id != user_id
        return RouterDeckGetReturn(deck=deck, deck_cards=deck_cards, read_only=read_only)
    
    @staticmethod
    async def update(db: AsyncSession, user_id:int, deck_id: int, deck: RouterDeckUpdate) -> RouterDeckUpdateReturn:
        db_deck = await DeckCrud.get(db=db, deck_id=deck_id)
        if db_deck is None or db_deck.user_id != user_id:
            return None
        try:
            deck_info = DeckUpdate(deck_name=deck.deck_name, image_path=deck.image_path, is_public=deck.is_public)
            result_deck = await DeckCrud.update(db=db,deck_id=deck_id, deck=deck_info)
            result_cards:list[DeckCard] = await DeckCardCrud.update_all(db=db,deck_id=deck_id, cards=deck.deck_cards)
            await db.commit()
            await db.refresh(result_deck)
            if result_deck is None:
                return None
            for result_card in result_cards:
                await db.refresh(result_card)
            
        except Exception as e:
            await db.rollback()
            raise e
        return RouterDeckUpdateReturn(deck= result_deck, deck_cards={card.card_id: card.card_count for card in result_cards})
    
    @staticmethod
    async def create(db: AsyncSession, user_id:int, deck:RouterDeckCreate):
        try:
            deck_data = DeckCreate(user_id=user_id, deck_name=deck.deck_name, image_path=deck.image_path)
            deck = await DeckCrud.create(db, deck=deck_data)
            await db.commit()
            await db.refresh(deck)
        except Exception as e:
            await db.rollback()
            raise e
        return deck
    
    
    @staticmethod
    async def get_cards(db: AsyncSession, deck_id: int) -> dict[int,int]:
        logger.warning(f"\n\n{deck_id}\n\n")
        deck_cards: list[DeckCard] = await DeckCardCrud.get_all(db=db, deck_id=deck_id)
        for card in deck_cards:
            await db.refresh(card)
        return {deck_card.card_id:deck_card.card_count for deck_card in deck_cards}