from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from models import DeckCard
from schemas.deck_cards import DeckCardCreate, DeckCardUpdate


class deck_card_crud:

    @staticmethod
    async def get(db: AsyncSession, deck_id: int, card_id:int) -> DeckCard | None:
        result = await db.execute(select(DeckCard).filter_by(deck_id=deck_id,card_id = card_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, deck_card: DeckCardCreate) -> DeckCard:
        db_deck_card = DeckCard(**deck_card.model_dump())
        db.add(db_deck_card)
        return db_deck_card

    @staticmethod
    async def update(db: AsyncSession, deck_card_id: int, deck_card: DeckCardUpdate):
        db_deck_card = await db.get(DeckCard, deck_card_id)
        if db_deck_card:
            for key, value in deck_card.model_dump().items():
                setattr(db_deck_card, key, value)
            return db_deck_card
        return None

    @staticmethod
    async def delete(db: AsyncSession, deck_card_id : int):
        db_deck_card = await db.get(DeckCard, deck_card_id)
        if db_deck_card:
            await db.delete(db_deck_card)
            return db_deck_card
        return None

    @staticmethod
    async def get_all(db: AsyncSession, deck_id: int) -> list[DeckCard] | None:
        result = await db.execute(select(DeckCard).filter(DeckCard.deck_id == deck_id))
        return result.scalars().all()


    @staticmethod
    async def create_all(db: AsyncSession, deck_id: int, cards_ids: list[int]):
        db.add_all(
            [DeckCard(deck_id=deck_id, card_id=card_id) for card_id in cards_ids]
        )
    @staticmethod
    async def delete_all(db: AsyncSession, deck_id : int):
        await db.execute(delete(DeckCard).filter(DeckCard.deck_id == deck_id))


    async def update_all(db: AsyncSession, deck_id: int, cards: dict[int, int]):
        existing_deck_cards = await deck_card_crud.get_all(db, deck_id)
        existing_card_ids = {deck_card.card_id for deck_card in existing_deck_cards}

        new_card_ids = set(cards.keys())
        cards_to_add = new_card_ids - existing_card_ids
        cards_to_remove = existing_card_ids - new_card_ids

        # 삭제할 카드들 처리
        if cards_to_remove:
            await db.execute(delete(DeckCard).filter(
                DeckCard.deck_id == deck_id,
                DeckCard.card_id.in_(cards_to_remove)
            ))

        # 추가할 카드들 처리
        new_cards = []
        if cards_to_add:
            new_cards = [DeckCard(deck_id=deck_id, card_id=card_id, card_count=cards[card_id]) for card_id in cards_to_add]
            db.add_all(new_cards)

        # 기존 카드들 업데이트
        for deck_card in existing_deck_cards:
            if deck_card.card_id in cards:
                deck_card.card_count = cards[deck_card.card_id]

        return existing_deck_cards + new_cards