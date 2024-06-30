# server/routers/decks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..DB.database import get_db
from ..DB.schemas import Deck, DeckCreate, DeckUpdate, DeckUpdateReturn
from ..services.decks import create_deck, get_deck, update_deck, delete_deck
from ..auth import get_current_active_user, User
from ..utils import handle_transaction

router = APIRouter()

@router.post("/decks/", response_model=Deck)
async def create_deck_route(deck: DeckCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return await handle_transaction(db, create_deck, deck)

@router.get("/decks/{player_id}", response_model=list[Deck])
async def read_deck_route(player_id: int, db: AsyncSession = Depends(get_db)):
    return await get_deck(db=db, player_id=player_id)

@router.put("/decks/{deck_id}", response_model=DeckUpdateReturn)
async def update_deck_route(deck_id: int, deck: DeckUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return await handle_transaction(db, update_deck, deck_id, deck)

@router.delete("/decks/{deck_id}", response_model=Deck)
async def delete_deck_route(deck_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return await handle_transaction(db, delete_deck, deck_id)