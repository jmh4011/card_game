import asyncio
from schemas.game.enums import ZoneType
from schemas.game.games import ConditionInfo
from modules.card import Card
from modules.registry import get_effect
from modules.effect import Effect


class EffectManager:
    def __init__(self):
        self.prepared_effects: dict[ZoneType, list[Effect]] = {zone: [] for zone in ZoneType}
        
    async def on_card_moved(self, card: Card, new_zone: ZoneType):
        for effect in card.effects:
            if card.zone in effect.zones:
                self.prepared_effects[card.zone].remove(effect)
            if new_zone in effect.zones:
                self.prepared_effects[new_zone].append(effect)

    async def effects_check(self, cards: list[Card]):
        for card in cards:
            for effect in card.effects: 
                if card.zone in effect.zones:
                    self.prepared_effects[card.zone].extend(effect)

    async def get_available_effects(self, condition_info: ConditionInfo) -> dict[ZoneType, list[Effect]]:
        tasks = []

        # 각 효과의 조건을 병렬로 체크하는 작업을 생성
        for key, effects in self.prepared_effects.items():
            tasks.append(self._check_effects_in_zone(key, effects, condition_info))

        # 병렬로 작업 실행
        results = await asyncio.gather(*tasks)

        return {zone:effects for zone, effects in results}

    async def _check_effects_in_zone(
        self, 
        zone: ZoneType, 
        effects: list[Effect], 
        condition_info: ConditionInfo
    ) -> tuple[ZoneType, list[Effect]]:
        
        results = await asyncio.gather(
            *[self._condition_check(effect=effect, condition_info=condition_info) for effect in effects]
        )

        return zone, results

    async def _condition_check(self, effect: Effect, condition_info: ConditionInfo) -> bool:
        if await effect.condition(condition_info):
            return effect
    