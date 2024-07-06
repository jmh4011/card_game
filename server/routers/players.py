# server/routers/players.py
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas.players import Player, PlayerCreate, PlayerUpdate
from ..schemas.player_stats import PlayerStats
from ..schemas.player_cards import PlayerCardReturn
from ..services import player_services
from ..auth import get_password_hash
from ..utils import handle_transaction

router = APIRouter()

@router.post("/players/login", response_model=str)
async def login_player_route(response: Response, player: PlayerCreate, db: AsyncSession = Depends(get_db)):
    access_token,refresh_token = player_services.login(db=db, player=player)
    if access_token:
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return refresh_token
    raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/players/create", response_model=int)
async def create_player_route(response: Response, player: PlayerCreate, db: AsyncSession = Depends(get_db)):
    access_token,refresh_token = player_services.create(db=db, player=player)
    if access_token:
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return refresh_token
    raise HTTPException(
            status_code=401,
            detail="Invalid username",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/players/state/{player_id}", response_model=PlayerStats)
async def read_player_state_route(player_id: int, db: AsyncSession = Depends(get_db)):
    return await get_player(db=db, player_id=player_id)

@router.get("/players/cards/{player_id}", response_model=list[PlayerCardReturn])
async def read_player_cards_route(player_id: int, db: AsyncSession = Depends(get_db)):
    return await get_player(db=db, player_id=player_id)
