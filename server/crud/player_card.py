from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, delete
from models import PlayerCard
from schemas.player_cards import PlayerCardCreate, PlayerCardUpdate

class PlayerCardCrud:

    @staticmethod
    async def get(db: AsyncSession, player_id: int, card_id: int):
        db_player_card = await db.execute(select(PlayerCard).filter_by(player_id=player_id, card_id=card_id))
        return db_player_card.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, player_card: PlayerCardCreate):
        db_player_card = PlayerCard(**player_card.model_dump())
        db.add(db_player_card)
        return db_player_card

    @staticmethod
    async def update(db: AsyncSession, player_card_id: int, player_card: PlayerCardUpdate):
        db_player_card = await db.get(PlayerCard, player_card_id)
        if db_player_card:
            for key, value in player_card.model_dump().items():
                setattr(db_player_card, key, value)
            return db_player_card
        return None

    @staticmethod
    async def delete(db: AsyncSession, player_card_id: int):
        player_card = await db.get(PlayerCard, player_card_id)
        if player_card:
            await db.delete(player_card)
            return player_card
        return None

    @staticmethod
    async def get_all(db: AsyncSession, player_id: int):
        result = await db.execute(select(PlayerCard).filter(PlayerCard.player_id == player_id))
        return result.scalars().all()

    @staticmethod
    async def delete_all(db: AsyncSession, player_id: int):
        await db.execute(delete(PlayerCard).filter(PlayerCard.player_id == player_id))

    @staticmethod
    async def add(db: AsyncSession, player_id: int, card_id: int):
        db_player_card = await db.execute(select(PlayerCard).filter_by(player_id=player_id, card_id=card_id))
        existing_card = db_player_card.scalar_one_or_none()
        if existing_card:
            existing_card.card_count += 1
            return existing_card
        else:
            new_card = PlayerCard(player_id=player_id, card_id=card_id, card_count=1)
            db.add(new_card)
            return new_card

    @staticmethod
    async def sub(db: AsyncSession, player_id: int, card_id: int):
        db_player_card = await db.execute(select(PlayerCard).filter_by(player_id=player_id, card_id=card_id))
        existing_card = db_player_card.scalar_one_or_none()
        if existing_card:
            if existing_card.card_count > 1:
                existing_card.card_count -= 1
                return existing_card
            else:
                await db.execute(delete(PlayerCard).filter_by(player_id=player_id, card_id=card_id))
                return None

    @staticmethod
    async def search_players(db: AsyncSession, **kwargs) -> list[PlayerCard] | None:
        conditions = []
        for field, value in kwargs.items():
            if field not in PlayerCard.__table__.columns.keys():
                return None
            conditions.append(getattr(PlayerCard, field) == value)
        
        stmt = select(PlayerCard).where(and_(*conditions))
        result = await db.execute(stmt)
        db_players = result.scalars().all()
        
        return db_players
