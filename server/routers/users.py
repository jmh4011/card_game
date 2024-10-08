from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from auth import set_auth_cookies
from database import get_db
from schemas.db.users import UserCreate
from schemas.router.users import UserLogin, UserSignUp
from schemas.db.user_stats import UserStatSchemas
from schemas.router.user_stats import RouterUserStatUpdate
from schemas.db.user_deck_selections import UserDeckSelectionUpdate
from schemas.db.decks import DeckSchemas
from services import UserServices
from auth import get_user_id


router = APIRouter()

@router.get("/users/auth", response_model=bool)
async def auth_user_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db,request=request,response=response)
    return True


@router.put("/users/login", response_model=str)
async def login_user_route(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    result = await UserServices.login(db=db, user=user)
    if result:
        access_token, refresh_token = result
        await set_auth_cookies(response=response, access_token=access_token, refresh_token=refresh_token)
        return "Login successful"
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/users/signup", response_model=str)
async def create_user_route(user: UserSignUp, response: Response, db: AsyncSession = Depends(get_db)):
    result = await UserServices.signup(db=db, user=user)
    if result:
        access_token, refresh_token = result
        await set_auth_cookies(response=response, access_token=access_token, refresh_token=refresh_token)
        return "user created successfully"
    raise HTTPException(
        status_code=401,
        detail="Invalid username",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.delete("/users/logout", response_model=str)
async def logout_user_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db,request=request,response=response)
    await UserServices.update_refresh_token(db=db,user_id=user_id, refresh_token=None)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return 'Logout successful'

@router.get("/users/stat", response_model=UserStatSchemas)
async def read_user_state_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    stats = await UserServices.get_stat(db=db, user_id=user_id)
    if stats is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return stats

@router.put("/users/stat", response_model=UserStatSchemas)
async def update_user_state_route(data: RouterUserStatUpdate, request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    stats = await UserServices.update_stat(db=db, user_id=user_id, data=data)
    if stats is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return stats



@router.get("/users/cards", response_model=dict[int,int])
async def read_user_cards_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    cards = await UserServices.get_cards(db=db, user_id=user_id)
    if cards is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return cards



@router.get("/users/deck-selection", response_model=dict[int,DeckSchemas])
async def read_user_deck_selection_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    decks = await UserServices.get_deck_selection_all(db=db, user_id=user_id)
    if decks is None:
        raise []
    return decks

@router.get("/users/deck-selection/{mod_id}", response_model=DeckSchemas)
async def read_user_deck_selection_route(mod_id: int,request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    deck = await UserServices.get_deck_selection(db=db, user_id=user_id, mod_id=mod_id)
    if deck is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="deck not found")
    return deck

@router.put("/users/deck-selection", response_model=DeckSchemas)
async def read_user_deck_selection_route(data:UserDeckSelectionUpdate, request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    result = await UserServices.set_deck_selection(db=db, user_id=user_id, data=data)
    return result
