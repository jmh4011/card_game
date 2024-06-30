from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from server.utils import to_dict
from ..schemas import PlayerCardReturn
from ..models import DeckCard
from ..crud import player_cards as crud_player_cards, cards as crud_cards
from sqlalchemy.ext.declarative import DeclarativeMeta

async def get_deck_cards(db: AsyncSession, deck_id: int):
    result = await db.execute(select(DeckCard).filter(DeckCard.deck_id == deck_id))
    return result.scalars().all()

async def create_deck_cards(db: AsyncSession, deck_id: int, cards_ids: list[int]):
    db.add_all(
        [DeckCard(deck_id=deck_id, card_id=card_id) for card_id in cards_ids]
    )

async def delete_deck_cards(db: AsyncSession, deck_id: int):
    await db.execute(delete(DeckCard).filter(DeckCard.deck_id == deck_id))

async def update_deck_cards(db: AsyncSession, deck_id: int, deck_cards_id: list[int]):
    existing_deck_cards = await get_deck_cards(db, deck_id)
    existing_card_ids = {deck_card.card_id for deck_card in existing_deck_cards}

    new_card_ids = set(deck_cards_id)
    cards_to_add = new_card_ids - existing_card_ids
    cards_to_remove = existing_card_ids - new_card_ids

    # Remove cards that are no longer in the deck
    if cards_to_remove:
        await db.execute(delete(DeckCard).filter(
            DeckCard.deck_id == deck_id,
            DeckCard.card_id.in_(cards_to_remove)
        ))

    # Add new cards to the deck
    if cards_to_add:
        db.add_all(
            [DeckCard(deck_id=deck_id, card_id=card_id) for card_id in cards_to_add]
        )

async def deck_cards_to_player_cards(db: AsyncSession, deck_id: int, player_id: int):
    db_deck_cards = await get_deck_cards(db, deck_id)
    deck_cards_return = []

    for db_card in db_deck_cards:
        card_info = await crud_cards.get_card(db=db, card_id=db_card.card_id)
        card_info_dict = await to_dict(card_info, db)
        db_player_card = await crud_player_cards.search_players(db=db, player_id=player_id, card_id=db_card.card_id)
        if db_player_card:
            card_info_dict['card_count'] = db_player_card[0].card_count
        else:
            card_info_dict['card_count'] = 0
        deck_cards_return.append(PlayerCardReturn(**card_info_dict))
    
    return deck_cards_return