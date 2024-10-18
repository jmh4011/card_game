from enum import Enum
from pydantic import BaseModel
from schemas.game.entity import Entity
from schemas.game.trigger_cards import TriggerCards
from schemas.game.target_info import TargetInfo


class ConditionInfo(BaseModel):
    player_id: int
    trigger_cards: TriggerCards

class EffectInfo(BaseModel):
    player_id: int
    targets: list[TargetInfo]

class ChainInfo(BaseModel):
    effect_id: int
    effect_info: EffectInfo

