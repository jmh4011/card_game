from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.auth import set_auth_cookies
from ..database import get_db
from ..schemas.players import PlayerCreate, PlayerLogin
from ..schemas.player_stats import PlayerStats
from ..schemas.player_cards import PlayerCardReturn
from ..services import player_services
from ..utils import handle_transaction, handle_token_refresh

router = APIRouter()

@router.post("/players/login", response_model=str)
async def login_player_route(response: Response, player: PlayerLogin, db: AsyncSession = Depends(get_db)):
    result = await handle_transaction(db, player_services.login, player=player)
    if result:
        access_token, refresh_token = result
        set_auth_cookies(response=response, access_token=access_token, refresh_token=refresh_token)
        return "Login successful"
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/players/create", response_model=str)
async def create_player_route(response: Response, player: PlayerCreate, db: AsyncSession = Depends(get_db)):
    result = await handle_transaction(db, player_services.create, player=player)
    if result:
        access_token, refresh_token = result
        set_auth_cookies(response=response, access_token=access_token, refresh_token=refresh_token)
        return "User created successfully"
    
    raise HTTPException(
        status_code=401,
        detail="Invalid username",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/players/state", response_model=PlayerStats)
async def read_player_state_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    player_id = await handle_token_refresh(db=db, request=request, response=response)
    
    stats = await player_services.get_stats(db=db, player_id=player_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Player not found")
    return stats

@router.get("/players/cards", response_model=list[PlayerCardReturn])
async def read_player_cards_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    player_id = await handle_token_refresh(db=db, request=request, response=response)

    cards = await player_services.get_cards(db=db, player_id=player_id)
    if not cards:
        raise HTTPException(status_code=404, detail="Player not found")
    return cards
