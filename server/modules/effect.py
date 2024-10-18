from typing import TYPE_CHECKING
from schemas.game.enums import ZoneType
from schemas.game.effect_info import ConditionInfo, EffectInfo
from schemas.game.entity import Entity
if TYPE_CHECKING:
    from modules.game_manager import GameManager
    
class Effect:
    def __init__(self,
                game_manager:'GameManager', 
                instance_id:int, 
                effect_id:int, 
                card_id:int, 
                zones:list[ZoneType], 
                select:bool) -> None:
        self.game_manager = game_manager
        self.instance_id = instance_id
        self.effect_id = effect_id
        self.card_id = card_id
        self.zones = zones
        self.select = select

    async def before(self, effect_info: 'EffectInfo'):
        pass

    async def after(self, effect_info: 'EffectInfo'):
        pass
    
    async def condition(self, condition_info: 'ConditionInfo') -> bool:
        return False
    
    async def targets(self, condition_info: 'ConditionInfo') -> list[Entity]:
        return []
    