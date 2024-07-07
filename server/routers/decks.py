# server/routers/decks.py
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas.routers import RouterDeckUpdate
from ..services import deck_services
from ..utils import handle_token_refresh

router = APIRouter()

@router.get("/decks/")
async def read_deck_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    player_id = await handle_token_refresh(db=db, request=request, response=response)
    
    decks = await deck_services.get(db=db, player_id=player_id)
    if not decks:
        raise HTTPException(status_code=404, detail="Deck not found")
    return decks

@router.put("/decks/{deck_id}")
async def update_deck_route(deck_id :int, deck: RouterDeckUpdate, request: Request, response: Response,  db: AsyncSession = Depends(get_db)):
    player_id = await handle_token_refresh(db=db, request=request, response=response)
    deck = await deck_services.update(db=db, deck_id=deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck
