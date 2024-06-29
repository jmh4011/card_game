from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import cards as crud_cards
from ..schemas import Card, CardCreate

router = APIRouter()

@router.post("/cards/", response_model=Card)
async def create_card(card: CardCreate, db: AsyncSession = Depends(get_db)):
    db_card = await crud_cards.create_card(db=db, card=card)
    await db.commit()  # 명시적으로 commit 수행
    await db.refresh(db_card)
    return db_card

@router.get("/cards/", response_model=list[Card])
async def read_cards(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud_cards.get_cards(db=db, skip=skip, limit=limit)

@router.get("/cards/{card_id}", response_model=Card)
async def read_card(card_id: int, db: AsyncSession = Depends(get_db)):
    db_card = await crud_cards.get_card(db=db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card

@router.put("/cards/{card_id}", response_model=Card)
async def update_card(card_id: int, card: CardCreate, db: AsyncSession = Depends(get_db)):
    db_card = await crud_cards.update_card(db=db, card_id=card_id, card=card)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    await db.commit()  # 명시적으로 commit 수행
    await db.refresh(db_card)
    return db_card

@router.delete("/cards/{card_id}", response_model=Card)
async def delete_card(card_id: int, db: AsyncSession = Depends(get_db)):
    db_card = await crud_cards.delete_card(db=db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    await db.commit()  # 명시적으로 commit 수행
    return db_card
