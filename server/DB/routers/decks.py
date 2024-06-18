from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import decks as crud_decks
from ..schemas import Deck, DeckCreate, DeckUpdate, DeckCard, DeckCardCreate, DeckCardUpdate

router = APIRouter()


@router.post("/decks/", response_model=Deck)
async def create_deck(deck: DeckCreate, db: Session = Depends(get_db)):
    return await crud_decks.create_deck(db=db, deck=deck)


@router.get("/decks/{player_id}", response_model=list[Deck])
async def read_deck(player_id: int, db: Session = Depends(get_db)):
    db_deck = await crud_decks.get_deck(db=db, player_id=player_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck

@router.put("/decks/{deck_id}", response_model=Deck)
async def update_deck(deck_id: int, deck: DeckUpdate, db: Session = Depends(get_db)):
    db_deck = await crud_decks.update_deck(db=db, deck_id=deck_id, deck=deck)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck



