from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from auth import set_auth_cookies
from database import get_db
from schemas.users import UserCreate, UserLogin
from schemas.user_stats import UserStats
from schemas.user_cards import UserCardReturn
from services import UserServices
from auth import get_user_id


router = APIRouter()



@router.put("/users/login", response_model=str)
async def login_user_route(response: Response, user: UserLogin, db: AsyncSession = Depends(get_db)):
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

@router.post("/users/create", response_model=str)
async def create_user_route(response: Response, user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await UserServices.create(db=db, user=user)
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
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    await UserServices.update_refresh_token(db=db,user_id=user_id, refresh_token=None)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return 'Logout successful'

@router.get("/users/state", response_model=UserStats)
async def read_user_state_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    stats = await UserServices.get_stats(db=db, user_id=user_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="User not found")
    return stats

@router.get("/users/cards", response_model=dict[int,int])
async def read_user_cards_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    cards = await UserServices.get_cards(db=db, user_id=user_id)
    if cards is None:
        raise HTTPException(status_code=404, detail="user not found")
    return cards
