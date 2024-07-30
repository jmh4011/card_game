from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from auth import set_auth_cookies
from database import get_db
from schemas.players import PlayerCreate, PlayerLogin
from schemas.player_stats import PlayerStats
from schemas.player_cards import PlayerCardReturn
from services import PlayerServices
from auth import get_player_id


router = APIRouter()



@router.put("/players/login", response_model=str)
async def login_player_route(response: Response, player: PlayerLogin, db: AsyncSession = Depends(get_db)):
    result = await PlayerServices.login(db=db, player=player)
    if result:
        access_token, refresh_token = result
        await set_auth_cookies(response=response, access_token=access_token, refresh_token=refresh_token)
        return "Login successful"
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/players/create", response_model=str)
async def create_player_route(response: Response, player: PlayerCreate, db: AsyncSession = Depends(get_db)):
    result = await PlayerServices.create(db=db, player=player)
    if result:
        access_token, refresh_token = result
        await set_auth_cookies(response=response, access_token=access_token, refresh_token=refresh_token)
        return "User created successfully"
    raise HTTPException(
        status_code=401,
        detail="Invalid username",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.delete("/players/logout", response_model=str)
async def logout_player_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    player_id = await get_player_id(db=db,request=request,response=response)
    if player_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    await PlayerServices.update_refresh_token(db=db,player_id=player_id, refresh_token=None)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return 'Logout successful'

@router.get("/players/state", response_model=PlayerStats)
async def read_player_state_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    player_id = await get_player_id(db=db, request=request, response=response)
    if player_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    stats = await PlayerServices.get_stats(db=db, player_id=player_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return stats

@router.get("/players/cards", response_model=dict[int,int])
async def read_player_cards_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    player_id = await get_player_id(db=db, request=request, response=response)
    if player_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    cards = await PlayerServices.get_cards(db=db, player_id=player_id)
    if cards is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return cards
