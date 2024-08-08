from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import GameMode
from schemas.game_modes import GameModeCreate, GameModeUpdate


class GameModeCrud:
    @staticmethod
    async def get(db: AsyncSession, mode_id: int):
        db_game = await db.execute(select(GameMode).where(GameMode.mode_id == mode_id))
        return db_game.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, card: GameModeCreate):
        db_game = GameMode(**card.model_dump())
        db.add(db_game)
        return db_game

    @staticmethod
    async def update(db: AsyncSession, mode_id: int, game_mode: GameModeUpdate):
        db_game = await db.get(GameMode, mode_id)
        if db_game:
            for key, value in game_mode.model_dump().items():
                setattr(db_game, key, value)
            return db_game
        return None

    @staticmethod
    async def delete(db: AsyncSession, mode_id: int):
        db_game = await db.get(GameMode, mode_id)
        if db_game:
            await db.delete(db_game)
            return db_game
        return None
    
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(GameMode))
        return result.scalars().all()