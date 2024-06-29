from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import players as crud_players
from ..crud import player_stats as crud_player_stats
from ..crud import player_cards as crud_player_cards
from ..crud import cards as crud_cards
from ..schemas import Player, PlayerBase, PlayerCreate, PlayerUpdate, PlayerStatsCreate, PlayerStats, PlayerCardReturn
import bcrypt

router = APIRouter()

async def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def to_dict(instance):
    if isinstance(instance.__class__, DeclarativeMeta):
        return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}
    else:
        raise ValueError("The provided instance is not a SQLAlchemy model.")

@router.get("/players/{player_id}", response_model=Player)
async def read_player(player_id: int, db: AsyncSession = Depends(get_db)):
    db_player = await crud_players.get_player(db=db, player_id=player_id)
    if db_player:
        return db_player
    raise HTTPException(status_code=404, detail="Player not found")

@router.put("/players/{player_id}", response_model=Player)
async def update_player(player_id: int, player: PlayerUpdate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        db_player = await crud_players.update_player(db=db, player_id=player_id, player=player)
    if db_player:
        await db.commit()
        await db.refresh(db_player)
        return db_player
    raise HTTPException(status_code=404, detail="Player not found")

@router.delete("/players/{player_id}", response_model=Player)
async def delete_player(player_id: int, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        db_player = await crud_players.delete_player(db=db, player_id=player_id)
        await crud_player_stats.delete_player_stats(db=db, player_id=player_id)
        await crud_player_cards.delete_player_cards(db=db, player_id=player_id)
    if db_player:
        await db.commit()
        return db_player
    raise HTTPException(status_code=404, detail="Player not found")

@router.post("/players/login", response_model=int)
async def login_player(player: PlayerBase, db: AsyncSession = Depends(get_db)):
    db_player = await crud_players.search_players(db=db, username=player.username)
    if db_player and await verify_password(player.password, db_player[0].password):
        return db_player[0].player_id
    return -1

@router.put("/players/create/{username}/{password}", response_model=int)
async def create_player(username: str, password: str, db: AsyncSession = Depends(get_db)):
    db_player = await crud_players.search_players(db=db, username=username)
    if db_player:
        return -1
    hashed_password = await hash_password(password)
    player_create = PlayerCreate(username=username, password=hashed_password)
    async with db.begin():
        db_player = await crud_players.create_player(db=db, player=player_create)
        player_stats_create = PlayerStatsCreate(player_id=db_player.player_id, current_deck_id=None, money=0)
        await crud_player_stats.create_player_stats(db=db, stats=player_stats_create)
    await db.commit()
    return db_player.player_id

@router.get("/players/state/{player_id}", response_model=PlayerStats)
async def read_player_state(player_id: int, db: AsyncSession = Depends(get_db)):
    db_player = await crud_player_stats.get_player_stats(db=db, player_id=player_id)
    if db_player:
        return db_player
    raise HTTPException(status_code=404, detail="Player not found")

@router.get("/players/cards/{player_id}", response_model=list[PlayerCardReturn])
async def read_player_cards(player_id:int, db: AsyncSession = Depends(get_db)):
    db_player_cards = await crud_player_cards.get_player_cards(db=db, player_id=player_id)
    db_player_cards_return = []

    for i in db_player_cards:
        card_info = await crud_cards.get_card(db=db, card_id=i.card_id)
        card_info_dict = to_dict(card_info)
        card_info_dict['card_count'] = i.card_count
        db_player_cards_return.append(PlayerCardReturn(**card_info_dict))

    return db_player_cards_return
