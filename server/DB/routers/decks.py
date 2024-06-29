from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import get_db
from ..crud import decks as crud_decks
from ..crud import deck_cards as crud_deck_cards
from ..crud import player_cards as crud_player_cards
from ..crud import cards as crud_cards
from ..schemas import Deck, DeckCreate, DeckUpdate, DeckCard, DeckUpdateReturn, PlayerCardReturn
from sqlalchemy.ext.declarative import DeclarativeMeta

router = APIRouter()

async def to_dict(instance, db: AsyncSession):
    if isinstance(instance.__class__, DeclarativeMeta):
        await db.refresh(instance)
        return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}
    else:
        raise ValueError("The provided instance is not a SQLAlchemy model.")

@router.post("/decks/", response_model=Deck)
async def create_deck(deck: DeckCreate, db: AsyncSession = Depends(get_db)):
    db_deck = await crud_decks.create_deck(db=db, deck=deck)
    await db.commit()
    await db.refresh(db_deck)
    return db_deck

@router.get("/decks/{player_id}", response_model=list[Deck])
async def read_deck(player_id: int, db: AsyncSession = Depends(get_db)):
    db_deck = await crud_decks.get_deck(db=db, player_id=player_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck


@router.put("/decks/{deck_id}", response_model=DeckUpdateReturn)
async def update_deck(deck_id: int, deck: DeckUpdate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        db_deck = await crud_decks.update_deck(db=db, deck_id=deck_id, deck=deck)
        if db_deck is None:
            raise HTTPException(status_code=404, detail="Deck not found")
        await crud_deck_cards.update_deck_cards(db=db, deck_id=deck_id, deck_cards_id=deck.deck_cards)
        db_deck_cards = await crud_deck_cards.deck_cards_to_player_cards(db=db, deck_id=deck_id, player_id=db_deck.player_id)
        await db.commit()

    deck_dict = await crud_deck_cards.to_dict(db_deck, db)
    deck_cards_dict = [await crud_deck_cards.to_dict(card, db) for card in db_deck_cards]

    return DeckUpdateReturn(deck=Deck(**deck_dict), deck_cards=[PlayerCardReturn(**card) for card in deck_cards_dict])

@router.get("/decks/cards/{deck_id}", response_model=list[DeckCard])
async def get_deck_cards(deck_id: int, db: AsyncSession = Depends(get_db)):
    db_cards = await crud_deck_cards.get_deck_cards(db=db, deck_id=deck_id)
    return db_cards

@router.get("/decks/cards/{deck_id}/{player_id}", response_model=list[PlayerCardReturn])
async def get_deck_cards_player(deck_id: int, player_id: int, db: AsyncSession = Depends(get_db)):
    db_cards = await crud_deck_cards.deck_cards_to_player_cards(db=db, deck_id=deck_id, player_id=player_id)
    return db_cards

@router.put("/decks/cards/{deck_id}", response_model=int)
async def update_deck_cards(deck_id: int, cards_id: list[int], db: AsyncSession = Depends(get_db)):
    async with db.begin():
        await crud_deck_cards.update_deck_cards(db=db, deck_id=deck_id, deck_cards_id=cards_id)
        await db.commit()
    return 1
