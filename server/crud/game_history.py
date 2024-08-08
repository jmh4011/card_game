from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import GameHistory
from schemas.game_historys import GameHistoryCreate, GameHistoryUpdate


class GameHistoryCrud:
    @staticmethod
    async def get(db: AsyncSession, game_id: int):
        db_game = await db.execute(select(GameHistory).where(GameHistory.game_id == game_id))
        return db_game.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, card: GameHistoryCreate):
        db_game = GameHistory(**card.model_dump())
        db.add(db_game)
        return db_game

    @staticmethod
    async def update(db: AsyncSession, game_id: int, game: GameHistoryUpdate):
        db_game = await db.get(GameHistory, game_id)
        if db_game:
            for key, value in game.model_dump().items():
                setattr(db_game, key, value)
            return db_game
        return None

    @staticmethod
    async def delete(db: AsyncSession, game_id: int):
        db_game = await db.get(GameHistory, game_id)
        if db_game:
            await db.delete(db_game)
            return db_game
        return None