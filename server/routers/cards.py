from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services import CardServices
from auth import get_user_id
from schemas.cards import CardRetrun


router = APIRouter()


@router.get("/cards", response_model=CardRetrun)
async def read_cards_all_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    cards = await CardServices.get(db=db)
    return cards

