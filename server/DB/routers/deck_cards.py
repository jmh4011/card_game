from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import deck_cards as crud_deck_cards
from ..schemas import DeckCard, DeckCardCreate, DeckCardUpdate

router = APIRouter()

@router.get("/decks/cards/{deck_id}", response_model=list[DeckCard])
async def get_deck_cards(deck_id: int, db: Session = Depends(get_db)):
    db_cards = await crud_deck_cards.get_deck_cards(db=db, deck_id=deck_id)
    return db_cards

@router.put("/decks/cards/{deck_id}", response_model=int)
async def update_deck_cards(deck_id:int, cards_id = list[int], db: Session = Depends(get_db)):
    await crud_deck_cards.delete_deck_cards(db=db,deck_id=deck_id)
    await crud_deck_cards.create_deck_cards(db=db,deck_id=deck_id,cards_id=cards_id)
    return 1
