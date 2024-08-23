# server/routers/decks.py
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.routers import RouterDeckUpdate, RouterDeckCreate, RouterDeckUpdateReturn
from schemas.decks import DeckSchemas
from services import DeckServices
from auth import get_user_id


router = APIRouter()

@router.get("/decks", response_model=list[DeckSchemas])
async def read_deck_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    decks = await DeckServices.get(db=db, user_id=user_id)
    if decks is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return decks

@router.put("/decks/{deck_id}", response_model=RouterDeckUpdateReturn)
async def update_deck_route(deck_id :int, deck: RouterDeckUpdate, request: Request, response: Response,  db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    deck = await DeckServices.update(db=db,user_id=user_id,deck_id=deck_id, deck=deck)
    return deck

@router.post("/decks", response_model=DeckSchemas)
async def create_deck_route(deck: RouterDeckCreate,request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    deck = await DeckServices.create(db=db,user_id=user_id, deck=deck)
    return deck


@router.get("/decks/cards/{deck_id}", response_model=dict[int,int])
async def read_deck_cards_route(deck_id:int,request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    deck_card = await DeckServices.get_cards(db=db, deck_id=deck_id)
    if deck_card is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck_card
