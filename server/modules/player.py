from sqlalchemy.ext.asyncio import AsyncSession
from modules.card import Card
from collections import deque
from modules.effect import Effect

from modules.registry import get_card_instnce

from modules.types import ZoneType, ConditionInfo, EffectInfo
import asyncio


class Player:
    def __init__(self, db: AsyncSession, user_id: int, cards: dict[int, int]) -> None:
        self.db = db
        self.user_id = user_id
        self.hands: deque[Card] = deque([])
        self.fields: deque[Card] = deque([])
        self.graves: deque[Card] = deque([])
        self.decks: deque[Card] = deque(
            get_card_instnce(card_id=key,zone=ZoneType.DECK, index=-1)
            for key, val in cards.items()
            for _ in range(val)
        )
        self.prepared_effects: dict[ZoneType, list[EffectInfo]] = {zone: [] for zone in ZoneType}
        self.effects_check(self.decks)

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

    def get_available_effects(self, condition_info: ConditionInfo) -> dict[ZoneType, list[EffectInfo]]:
        available_effects: dict[ZoneType, list[EffectInfo]] = {}
        for key, effect_infos in self.prepared_effects.items():
            available_effects[key] = [
                effect_info for effect_info in effect_infos
                if self._condition_check(effect_info=effect_info, condition_info=condition_info)
            ]
        return available_effects

    def _condition_check(self, effect_info: EffectInfo, condition_info: ConditionInfo) -> bool:
        return effect_info.effect.condition(condition_info)
