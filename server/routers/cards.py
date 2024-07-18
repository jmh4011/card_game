# server/routers/decks.py
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services import card_services
from auth import get_player_id
from schemas.cards import Card


router = APIRouter()


@router.get("/cards", response_model=dict[int,Card])
async def read_cards_all_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    player_id = await get_player_id(db=db, request=request, response=response)
    if player_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    cards = await card_services.get(db=db)
    return cards

