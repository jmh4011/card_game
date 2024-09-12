# server/routers/decks.py
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.router.decks import RouterDeckGetReturn, RouterDeckUpdate, RouterDeckCreate, RouterDeckUpdateReturn
from schemas.db.decks import DeckSchemas
from services import DeckServices
from auth import get_user_id


router = APIRouter()

@router.get("/decks", response_model=list[DeckSchemas])
async def read_deck_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    decks = await DeckServices.get_all(db=db, user_id=user_id)
    if decks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deck not found")
    return decks

@router.get("/decks/{deck_id}", response_model=RouterDeckGetReturn)
async def update_deck_route(deck_id :int, request: Request, response: Response,  db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    db_deck = await DeckServices.get(db=db, user_id=user_id, deck_id=deck_id)
    if db_deck is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deck not found")
    return db_deck

@router.put("/decks/{deck_id}", response_model=RouterDeckUpdateReturn)
async def update_deck_route(deck_id :int, deck: RouterDeckUpdate, request: Request, response: Response,  db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    db_deck = await DeckServices.update(db=db,user_id=user_id,deck_id=deck_id, deck=deck)
    return db_deck

@router.post("/decks", response_model=DeckSchemas)
async def create_deck_route(deck: RouterDeckCreate,request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    deck = await DeckServices.create(db=db,user_id=user_id, deck=deck)
    return deck


@router.get("/decks/cards/{deck_id}", response_model=dict[int,int])
async def read_deck_cards_route(deck_id:int,request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    deck_card = await DeckServices.get_cards(db=db, deck_id=deck_id)
    if deck_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deck Cards not found")
    return deck_card
