from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import GameMod
from schemas.db.game_mods import GameModCreate, GameModUpdate


class GameModCrud:
    @staticmethod
    async def get(db: AsyncSession, mod_id: int):
        db_game = await db.execute(select(GameMod).where(GameMod.mod_id == mod_id))
        return db_game.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, card: GameModCreate):
        db_game = GameMod(**card.model_dump())
        db.add(db_game)
        return db_game

    @staticmethod
    async def update(db: AsyncSession, mod_id: int, game_mod: GameModUpdate):
        db_game = await db.get(GameMod, mod_id)
        if db_game:
            for key, value in game_mod.model_dump().items():
                setattr(db_game, key, value)
            return db_game
        return None

    @staticmethod
    async def delete(db: AsyncSession, mod_id: int):
        db_game = await db.get(GameMod, mod_id)
        if db_game:
            await db.delete(db_game)
            return db_game
        return None
    
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(GameMod))
        return result.scalars().all()