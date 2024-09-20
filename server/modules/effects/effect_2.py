from typing import TYPE_CHECKING
from modules.effect import Effect
from schemas.game.enums import ZoneType
from schemas.game.effect_info import ConditionInfo
if TYPE_CHECKING:
    from modules.card import Card
    from modules.player import Player

class Effect_2(Effect):
    def __init__(self, card: Card, player: Player) -> None:
        super().__init__(card, player)
        self.effect_id = 1 
        self.zones = [ZoneType.HAND]
        self.select = True

    async def before(self, condition_info: ConditionInfo):
        pass

    async def after(self):
        pass
    
    async def condition(self, condition_info: ConditionInfo) -> tuple[bool,list]:
        return False,[]