from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, delete
from ..models import PlayerCard
from ..schemas import PlayerCardCreate

async def get_player_cards(db: AsyncSession, player_id: int):
    result = await db.execute(select(PlayerCard).filter(PlayerCard.player_id == player_id))
    return result.scalars().all()

async def create_player_cards(db: AsyncSession, player_id: int, cards_ids: list[int]):
    for card_id in cards_ids:
        db_player_card = await db.execute(select(PlayerCard).filter_by(player_id=player_id, card_id=card_id))
        existing_card = db_player_card.scalar_one_or_none()
        if existing_card:
            existing_card.card_count += 1
        else:
            db.add(PlayerCard(player_id=player_id, card_id=card_id))

async def delete_player_cards(db: AsyncSession, player_id: int):
    await db.execute(delete(PlayerCard).filter(PlayerCard.player_id == player_id))

async def add_player_card(db: AsyncSession, player_id: int, card_id: int):
    db_player_card = await db.execute(select(PlayerCard).filter_by(player_id=player_id, card_id=card_id))
    existing_card = db_player_card.scalar_one_or_none()
    if existing_card:
        existing_card.card_count += 1
    else:
        db.add(PlayerCard(player_id=player_id, card_id=card_id, card_count=1))

async def remove_player_card(db: AsyncSession, player_id: int, card_id: int):
    db_player_card = await db.execute(select(PlayerCard).filter_by(player_id=player_id, card_id=card_id))
    existing_card = db_player_card.scalar_one_or_none()
    if existing_card:
        if existing_card.card_count > 1:
            existing_card.card_count -= 1
        else:
            await db.execute(delete(PlayerCard).filter_by(player_id=player_id, card_id=card_id))

async def search_players(db: AsyncSession, **kwargs) -> list[PlayerCard]:
    conditions = []
    for field, value in kwargs.items():
        if field not in PlayerCard.__table__.columns.keys():
            return -1
        conditions.append(getattr(PlayerCard, field) == value)
    
    stmt = select(PlayerCard).where(and_(*conditions))
    result = await db.execute(stmt)
    db_players = result.scalars().all()
    
    return db_players
