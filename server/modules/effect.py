from typing import TYPE_CHECKING
from schemas.game.enums import ZoneType
from schemas.game.condition_info import ConditionInfo
if TYPE_CHECKING:
    from modules.card import Card


class Effect:
    def __init__(self, card:'Card') -> None:
        self.effect_id: int 
        self.card = card
        self.zones: list[ZoneType]
        self.select: bool

    async def before(self, condition_info: ConditionInfo):
        pass

    async def after(self):
        pass
    
    async def condition(self, condition_info: ConditionInfo) -> tuple[bool,list]:
        return False,[]