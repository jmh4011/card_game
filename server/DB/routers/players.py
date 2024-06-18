from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import players as crud_players
from ..crud import player_stats as crud_player_stats
from ..schemas import Player,PlayerBase, PlayerCreate, PlayerUpdate, PlayerStatsCreate

router = APIRouter()

@router.get("/players/{player_id}", response_model=Player)
async def read_player(player_id: int, db: AsyncSession = Depends(get_db)):
    db_player = await crud_players.get_player(db=db, player_id=player_id)
    if db_player:
        return db_player
    raise HTTPException(status_code=404, detail="Player not found")

@router.put("/players/{player_id}", response_model=Player)
async def update_player(player_id: int, player: PlayerUpdate, db: AsyncSession = Depends(get_db)):
    db_player = await crud_players.update_player(db=db, player_id=player_id, player=player)
    if db_player:
        return db_player
    raise HTTPException(status_code=404, detail="Player not found")

@router.delete("/players/{player_id}", response_model=Player)
async def delete_player(player_id: int, db: AsyncSession = Depends(get_db)):
    db_player = await crud_players.delete_player(db=db, player_id=player_id)
    db_player_stats = await crud_player_stats.delete_player_stats(db=db, player_id=player_id)
    if db_player:
        return db_player
    raise HTTPException(status_code=404, detail="Player not found")

@router.post("/players/login", response_model=int)
async def login_player(player:PlayerBase, db: AsyncSession = Depends(get_db)):
    db_player = await crud_players.search_players(db=db, username=player.username, password=player.password)
    if db_player:
        return db_player[0].player_id
    return -1

@router.put("/players/create", response_model=int)
async def create_player(player:PlayerBase, db: AsyncSession = Depends(get_db)):
    db_player = await crud_players.search_players(db=db, username=player.username)
    if db_player:
        return -1
    player_create = PlayerCreate(username=player.username, password=player.password)
    db_player = await crud_players.create_player(db=db, player=player_create)
    player_stats_create = PlayerStatsCreate(player_id=db_player.player_id)
    db_player_stats = await crud_player_stats.create_player_stats(db=db, stats=player_stats_create)
    return db_player.player_id
