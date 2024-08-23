from modules.player import Player
from modules.types import ZoneType, EffectInfo,ConditionInfo
from modules.card import Card


class EffectManager:
    def __init__(self):
        self.prepared_effects: dict[ZoneType, list[EffectInfo]] = {zone: [] for zone in ZoneType}
        
    def on_card_moved(self, card: Card, new_zone: ZoneType):
        for effect_info in card.effects:
            if card.zone in effect_info.zones:
                self.prepared_effects[card.zone].remove(effect_info)
            if new_zone in effect_info.zones:
                self.prepared_effects[new_zone].append(effect_info)
    
    def effects_check(self, cards: list[Card]):
        for card in cards:
            for effect_info in card.effects:
                if card.zone in effect_info.zones:
                    self.prepared_effects[card.zone].append(effect_info)
    
    def get_available_effects(self, condition_info:ConditionInfo):
        available_effects: dict[ZoneType, list[EffectInfo]] = {}
        for key, effect_infos in self.prepared_effects.items():
            available_effects[key] = [effect_info for effect_info in effect_infos
                                    if self.condition_check(effect_info=effect_info, condition_info=condition_info)]
            
            
    def condition_check(self, effect_info:EffectInfo, condition_info:ConditionInfo) -> bool:
        
        return effect_info.condition(condition_info)
    