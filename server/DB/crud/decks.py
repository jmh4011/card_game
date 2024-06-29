from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from ..models import Deck, DeckCard
from ..schemas import DeckCardCreate, DeckCreate, DeckUpdate

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

async def get_deck_cards(db: AsyncSession, deck_id: int):
    result = await db.execute(select(DeckCard).filter(DeckCard.deck_id == deck_id))
    return result.scalars().all()

async def create_deck_cards(db: AsyncSession, deck_id: int, cards_ids: list[int]):
    deck_cards = [DeckCard(deck_id=deck_id, card_id=card_id) for card_id in cards_ids]
    db.add_all(deck_cards)
    return deck_cards

async def delete_deck_cards(db: AsyncSession, deck_id: int):
    await db.execute(delete(DeckCard).filter(DeckCard.deck_id == deck_id))
    

async def update_deck_cards(db: AsyncSession, deck_id:int, deck_cards_id: list[int]):
    await db.execute(delete(DeckCard).filter(DeckCard.deck_id == deck_id))
    deck_cards = [DeckCard(deck_id=deck_id, card_id=card_id) for card_id in deck_cards_id]
    db.add_all(deck_cards)
    
    return deck_cards
