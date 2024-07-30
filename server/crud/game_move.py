# server/DB/crud/cards.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import GameMove
from schemas.game_moves import GameMoveCreate, GameMoveUpdate


class GameMoveCrud:
    @staticmethod
    async def get(db: AsyncSession, move_id: int):
        db_game_move = await db.execute(select(GameMove).where(GameMove.move_id == move_id))
        return db_game_move.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, card: GameMoveCreate):
        db_game_move = GameMove(**card.model_dump())
        db.add(db_game_move)
        return db_game_move

    @staticmethod
    async def update(db: AsyncSession, move_id: int, game_move: GameMoveUpdate):
        db_game_move = await db.get(GameMove, move_id)
        if db_game_move:
            for key, value in game_move.model_dump().items():
                setattr(db_game_move, key, value)
            return db_game_move
        return None

    @staticmethod
    async def delete(db: AsyncSession, move_id: int):
        db_game_move = await db.get(GameMove, move_id)
        if db_game_move:
            await db.delete(db_game_move)
            return db_game_move
        return None