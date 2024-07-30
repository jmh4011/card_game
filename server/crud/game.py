# server/DB/crud/cards.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Game
from schemas.games import GameCreate, GameUpdate


class GameCrud:
    @staticmethod
    async def get(db: AsyncSession, game_id: int):
        db_game = await db.execute(select(Game).where(Game.game_id == game_id))
        return db_game.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, card: GameCreate):
        db_game = Game(**card.model_dump())
        db.add(db_game)
        return db_game

    @staticmethod
    async def update(db: AsyncSession, game_id: int, game: GameUpdate):
        db_game = await db.get(Game, game_id)
        if db_game:
            for key, value in game.model_dump().items():
                setattr(db_game, key, value)
            return db_game
        return None

    @staticmethod
    async def delete(db: AsyncSession, card_id: int):
        db_game = await db.get(Game, card_id)
        if db_game:
            await db.delete(db_game)
            return db_game
        return None