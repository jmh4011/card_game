from typing import TYPE_CHECKING
from modules.effect import Effect
from schemas.game.enums import ZoneType
from schemas.game.effect_info import ConditionInfo, EffectInfo
if TYPE_CHECKING:
    from modules.card import Card

class Effect_2(Effect):
    def __init__(self, card: Card) -> None:
        super().__init__(
            effect_id=2,
            card=card,
            zones = [ZoneType.FIELD],
            select = True)

    async def before(self, effect_info: EffectInfo):
        self.card.player.adjust_cost(-1)

    async def after(self, effect_info: EffectInfo):
        entity = effect_info.targets[0].entity
        self.card.player.entity_to_card(entity=entity)
        self.card.move(ZoneType.FIELD, effect_info.targets[0].entity)
    
    async def condition(self, condition_info: ConditionInfo) -> bool:
        if self.card.player.cost >= 1:
            return True
        return False