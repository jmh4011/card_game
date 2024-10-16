from typing import TYPE_CHECKING
from schemas.game.enums import ZoneType
from schemas.game.effect_info import ConditionInfo, EffectInfo, TargetInfo
if TYPE_CHECKING:
    from modules.game_manager import GameManager
    
class Effect:
    def __init__(self,
                game_manager:'GameManager', 
                instance_id:int, 
                effect_id:int, 
                card:int, 
                zones:list[ZoneType], 
                select:bool) -> None:
        self.game_manager = game_manager
        self.instance_id = instance_id
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
    
    