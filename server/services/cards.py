from sqlalchemy.ext.asyncio import AsyncSession
from crud import CardCrud, EffectCrud, CardEffectCrud
from schemas.cards import CardSchemas, CardRetrun
from schemas.effects import EffectSchemas
from utils import to_dict

class CardServices:
    @staticmethod
    async def get(db: AsyncSession) -> CardRetrun:
        db_cards = await CardCrud.get_all(db=db)
        db_effects = await EffectCrud.get_all(db=db)
        db_card_effects = await CardEffectCrud.get_all(db=db)
        cards = {card.card_id: CardSchemas(**(await to_dict(card, db=db))) for card in db_cards}
        effects = {effect.effect_id: effect for effect in db_effects}
        for card_effect in db_card_effects:
            cards[card_effect.card_id].effects.append(card_effect.effect_id)
        return CardRetrun(cards=cards, effects=effects)
