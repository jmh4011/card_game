import asyncio
from modules.types import ZoneType, EffectInfo,ConditionInfo
from modules.card import Card


class EffectManager:
    def __init__(self):
        self.prepared_effects: dict[ZoneType, list[EffectInfo]] = {zone: [] for zone in ZoneType}
        
    def on_card_moved(self, card: Card, new_zone: ZoneType):
        for effect in card.effects:
            if card.zone in effect.zones:
                self.prepared_effects[card.zone].remove(EffectInfo(card=card, effect=effect))
            if new_zone in effect.zones:
                self.prepared_effects[new_zone].append(EffectInfo(card=card, effect=effect))

    def effects_check(self, cards: list[Card]):
        for card in cards:
            for effect in card.effects:
                if card.zone in effect.zones:
                    self.prepared_effects[card.zone].extend(EffectInfo(card=card, effect=effect))

    async def get_available_effects(self, condition_info: ConditionInfo) -> dict[ZoneType, list[EffectInfo]]:
        available_effects: dict[ZoneType, list[EffectInfo]] = {}
        tasks = []

        # 각 효과의 조건을 병렬로 체크하는 작업을 생성
        for key, effect_infos in self.prepared_effects.items():
            tasks.append(self._check_effects_in_zone(key, effect_infos, condition_info))

        # 병렬로 작업 실행
        results = await asyncio.gather(*tasks)

        # 결과를 수집
        for zone, effects in results:
            if effects:
                available_effects[zone] = effects

        return available_effects

    async def _check_effects_in_zone(
        self, 
        zone: ZoneType, 
        effect_infos: list[EffectInfo], 
        condition_info: ConditionInfo
    ) -> tuple[ZoneType, list[EffectInfo], list[list]]:
        
        results = await asyncio.gather(
            *[self._condition_check(effect_info=effect_info, condition_info=condition_info) for effect_info in effect_infos]
        )

        valid_effects = []
        collected_lists = []

        for effect_info, (is_valid, targets) in zip(effect_infos, results):
            if is_valid:
                effect_info.targets = targets
                valid_effects.append(effect_info)

        return zone, valid_effects, collected_lists

    async def _condition_check(self, effect_info: EffectInfo, condition_info: ConditionInfo) -> bool:
        return effect_info.effect.condition(condition_info)
    