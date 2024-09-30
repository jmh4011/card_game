from typing import TYPE_CHECKING
from schemas.game.enums import ZoneType
from schemas.game.effect_info import ConditionInfo, EffectInfo
if TYPE_CHECKING:
    from modules.card import Card

class Effect:
    def __init__(self, effect_id:int, card:'Card', zones:list[ZoneType], select:bool) -> None:
        self.effect_id = effect_id
        self.card = card
        self.zones = zones
        self.select = select
        self.targets = []

    async def before(self, effect_info: EffectInfo):
        pass

    async def after(self, effect_info: EffectInfo):
        pass
    
    async def condition(self, condition_info: ConditionInfo) -> bool:
        return False
    
    