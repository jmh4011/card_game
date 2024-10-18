import asyncio
import logging
from typing import TYPE_CHECKING
from modules.card import Card
from schemas.game.enums import ZoneType
from modules.effect import Effect
if TYPE_CHECKING:
    from schemas.game.effect_info import ConditionInfo
    from modules.game_manager import GameManager

logger = logging.getLogger(__name__)

class EffectManager:
    def __init__(self,game_manager : 'GameManager'):
        self.prepared_effects: dict[ZoneType, list[Effect]] = {zone: [] for zone in ZoneType}
        self.game_manager = game_manager

    async def on_card_moved(self, card_id: int) -> None:
        card = await self.game_manager.registry_manager.get_card_instance(card_id)
        for effect_id in card.effects:
            effect = await self.game_manager.registry_manager.get_effect_instance(effect_id)
            # 이전 존에서 효과 제거
            if card.before_zone in effect.zones and effect in self.prepared_effects[card.before_zone]:
                try:
                    self.prepared_effects[card.before_zone].remove(effect)
                except ValueError:
                    pass  # 효과가 목록에 없을 수 있습니다.
            # 새로운 존에 효과 추가
            if card.zone in effect.zones:
                self.prepared_effects[card.zone].append(effect)
    
    async def effects_check(self, cards: list[int]) -> None:
        """Initializes prepared effects from a list of cards."""
        for card_id in cards:
            card = await self.game_manager.registry_manager.get_card_instance(card_id)
            for effect_id in card.effects:
                effect = await self.game_manager.registry_manager.get_effect_instance(effect_id)
                if card.zone in effect.zones:
                    self.prepared_effects[card.zone].append(effect)

    async def get_available_effects(self, condition_info: 'ConditionInfo') -> list[int]:
        """Gets available effects based on the condition info."""
        available_effects = []
        for zone, effects in self.prepared_effects.items():
            available_effects += await self._check_effects_in_zone(effects, condition_info)
        return available_effects

    async def _check_effects_in_zone(self, effects: list[int], condition_info: 'ConditionInfo') -> list[int]:
        """Checks which effects are available in a specific zone."""
        results = await asyncio.gather(
            *[self._condition_check(effect, condition_info) for effect in effects]
        )
        # None 값을 제거하여 실제 효과만 남깁니다.
        available_effects = [effect for effect in results if effect is not None]
        return available_effects

    async def _condition_check(self, effect_id: int, condition_info: 'ConditionInfo') -> Effect | None:
        """Checks if an effect's condition is met."""
        effect = await self.game_manager.registry_manager.get_effect_instance(effect_id)
        if await effect.condition(condition_info):
            return effect_id
        return None
