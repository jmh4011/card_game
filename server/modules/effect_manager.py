import asyncio
from modules.card import Card
from schemas.game.condition_info import ConditionInfo
from schemas.game.enums import ZoneType
from modules.effect import Effect


class EffectManager:
    def __init__(self):
        self.prepared_effects: dict[ZoneType, list['Effect']] = {zone: [] for zone in ZoneType}

    async def on_card_moved(self, card: Card, new_zone: ZoneType) -> None:
        """Updates the prepared effects when a card moves zones."""
        if card.zone in card.before_zone and card.zone in self.prepared_effects:
            try:
                self.prepared_effects[card.before_zone].remove(card)
            except ValueError:
                pass  # 효과가 목록에 없을 수 있습니다.
        if new_zone in self.prepared_effects:
            self.prepared_effects[new_zone].append(card)

    async def effects_check(self, cards: list[Card]) -> None:
        """Initializes prepared effects from a list of cards."""
        for card in cards:
            for effect in card.effects:
                if card.zone in effect.zones:
                    self.prepared_effects[card.zone].append(effect)

    async def get_available_effects(
        self, condition_info: ConditionInfo
    ) -> dict[ZoneType, list['Effect']]:
        """Gets available effects based on the condition info."""
        tasks = [
            self._check_effects_in_zone(zone, effects, condition_info)
            for zone, effects in self.prepared_effects.items()
        ]
        results = await asyncio.gather(*tasks)
        return {zone: effects for zone, effects in results}

    async def _check_effects_in_zone(
        self, zone: ZoneType, effects: list['Effect'], condition_info: ConditionInfo
    ) -> tuple[ZoneType, list['Effect']]:
        """Checks which effects are available in a specific zone."""
        results = await asyncio.gather(
            *[self._condition_check(effect, condition_info) for effect in effects]
        )
        # None 값을 제거하여 실제 효과만 남깁니다.
        available_effects = [effect for effect in results if effect is not None]
        return zone, available_effects

    async def _condition_check(self, effect: 'Effect', condition_info: ConditionInfo) -> 'Effect':
        """Checks if an effect's condition is met."""
        if await effect.condition(condition_info):
            return effect
        return None
