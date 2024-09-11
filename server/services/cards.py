from sqlalchemy.ext.asyncio import AsyncSession
from crud import CardCrud, EffectCrud, CardEffectCrud
from schemas.db.cards import CardSchemas
from schemas.router.cards import CardRetrun
from schemas.db.effects import EffectSchemas
from models import CardEffect
from utils import to_dict

class CardServices:

    @staticmethod
    async def get(card_id:int, db: AsyncSession) -> CardSchemas:
        db_cards = await CardCrud.get(db=db, card_id=card_id)
        await db.refresh(db_cards)
        db_card_effects:list[CardEffect] = await CardEffectCrud.get(db=db, card_id=card_id)
        card = CardSchemas(**(await to_dict(db_cards, db=db)))
        for i in db_card_effects:
            await db.refresh(i)
        card.effects = [i.effect_id for i in db_card_effects]
        return card


    @staticmethod
    async def get_all(db: AsyncSession) -> CardRetrun:
        db_cards = await CardCrud.get_all(db=db)
        db_effects = await EffectCrud.get_all(db=db)
        db_card_effects = await CardEffectCrud.get_all(db=db)
        cards = {card.card_id: CardSchemas(**(await to_dict(card, db=db))) for card in db_cards}
        effects = {effect.effect_id: effect for effect in db_effects}
        for card_effect in db_card_effects:
            cards[card_effect.card_id].effects.append(card_effect.effect_id)
        return CardRetrun(cards=cards, effects=effects)

