import asyncio
import logging
from typing import TYPE_CHECKING
from modules.card import Card
from schemas.game.enums import ZoneType
from modules.effect import Effect
if TYPE_CHECKING:
    from schemas.game.effect_info import ConditionInfo

logger = logging.getLogger(__name__)

class EffectManager:
    def __init__(self):
        self.prepared_effects: dict[ZoneType, list[Effect]] = {zone: [] for zone in ZoneType}

    async def on_card_moved(self, card: Card) -> None:
        for effect in card.effects:
            # 이전 존에서 효과 제거
            if card.before_zone in effect.zones and effect in self.prepared_effects[card.before_zone]:
                try:
                    self.prepared_effects[card.before_zone].remove(effect)
                except ValueError:
                    pass  # 효과가 목록에 없을 수 있습니다.
            # 새로운 존에 효과 추가
            if card.zone in effect.zones:
                self.prepared_effects[card.zone].append(effect)
    
    async def effects_check(self, cards: list[Card]) -> None:
        """Initializes prepared effects from a list of cards."""
        for card in cards:
            for effect in card.effects:
                if card.zone in effect.zones:
                    self.prepared_effects[card.zone].append(effect)

    async def get_available_effects(self, condition_info: 'ConditionInfo') -> list[Effect]:
        """Gets available effects based on the condition info."""
        available_effects = []
        for zone, effects in self.prepared_effects.items():
            available_effects += await self._check_effects_in_zone(effects, condition_info)
        return available_effects

    async def _check_effects_in_zone(self, effects: list[Effect], condition_info: 'ConditionInfo') -> list[Effect]:
        """Checks which effects are available in a specific zone."""
        results = await asyncio.gather(
            *[self._condition_check(effect, condition_info) for effect in effects]
        )
        # None 값을 제거하여 실제 효과만 남깁니다.
        available_effects = [effect for effect in results if effect is not None]
        return available_effects

    async def _condition_check(self, effect: Effect, condition_info: 'ConditionInfo') -> Effect | None:
        """Checks if an effect's condition is met."""
        if await effect.condition(condition_info):
            return effect
        return None
