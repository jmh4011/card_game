# server/routers/players.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..DB.database import get_db
from ..DB.schemas import Player, PlayerCreate, PlayerUpdate, PlayerStats, PlayerCardReturn
from ..services.players import create_player, get_player, update_player, delete_player, search_players
from ..auth import get_password_hash, verify_password, get_current_active_user, User
from ..utils import handle_transaction

router = APIRouter()

@router.get("/players/{player_id}", response_model=Player)
async def read_player_route(player_id: int, db: AsyncSession = Depends(get_db)):
    return await get_player(db=db, player_id=player_id)

@router.put("/players/{player_id}", response_model=Player)
async def update_player_route(player_id: int, player: PlayerUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return await handle_transaction(db, update_player, player_id, player)

@router.delete("/players/{player_id}", response_model=Player)
async def delete_player_route(player_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return await handle_transaction(db, delete_player, player_id)

@router.post("/players/login", response_model=int)
async def login_player_route(player: PlayerCreate, db: AsyncSession = Depends(get_db)):
    user = await search_players(db=db, username=player.username)
    if user and verify_password(player.password, user[0].password):
        return user[0].player_id
    return -1

@router.put("/players/create/{username}/{password}", response_model=int)
async def create_player_route(username: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await search_players(db=db, username=username)
    if user:
        return -1
    hashed_password = get_password_hash(password)
    player_create = PlayerCreate(username=username, password=hashed_password)
    return await handle_transaction(db, create_player, player_create)

@router.get("/players/state/{player_id}", response_model=PlayerStats)
async def read_player_state_route(player_id: int, db: AsyncSession = Depends(get_db)):
    return await get_player(db=db, player_id=player_id)

@router.get("/players/cards/{player_id}", response_model=list[PlayerCardReturn])
async def read_player_cards_route(player_id: int, db: AsyncSession = Depends(get_db)):
    return await get_player(db=db, player_id=player_id)
