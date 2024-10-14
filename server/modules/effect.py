from typing import TYPE_CHECKING
from schemas.game.enums import ZoneType
if TYPE_CHECKING:
    from modules.card import Card  
    from schemas.game.effect_info import ConditionInfo, EffectInfo, TargetInfo

class Effect:
    def __init__(self, effect_id:int, card:'Card', zones:list[ZoneType], select:bool) -> None:
        self.effect_id = effect_id
        self.card = card
        self.zones = zones
        self.select = select
        self.targets: list['TargetInfo'] = []

    async def before(self, effect_info: 'EffectInfo'):
        pass

    async def after(self, effect_info: 'EffectInfo'):
        pass
    
    async def condition(self, condition_info: 'ConditionInfo') -> bool:
        return False
    
    