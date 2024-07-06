# server/routers/cards.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import Card, CardCreate
from ..services.cards import create_card, get_cards, get_card, update_card, delete_card
from ..auth import get_current_active_user, User
from ..utils import handle_transaction

router = APIRouter()

@router.post("/cards/", response_model=Card)
async def create_card_route(card: CardCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return await handle_transaction(db, create_card, card)

@router.get("/cards/", response_model=list[Card])
async def read_cards_route(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_cards(db=db, skip=skip, limit=limit)

@router.get("/cards/{card_id}", response_model=Card)
async def read_card_route(card_id: int, db: AsyncSession = Depends(get_db)):
    return await get_card(db=db, card_id=card_id)

@router.put("/cards/{card_id}", response_model=Card)
async def update_card_route(card_id: int, card: CardCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return await handle_transaction(db, update_card, card_id, card)

@router.delete("/cards/{card_id}", response_model=Card)
async def delete_card_route(card_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return await handle_transaction(db, delete_card, card_id)
