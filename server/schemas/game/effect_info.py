from pydantic import BaseModel, ConfigDict
from schemas.game.entity import Entity
from modules.effect import Effect
from schemas.game.trigger_cards import TriggerCards

class ConditionInfo(BaseModel):
    player: int
    opponent: int
    trigger_cards: TriggerCards

class TargetInfo(BaseModel):
    entity: Entity
    card: int | None


class EffectInfo(BaseModel):
    opponent: int
    targets: list[TargetInfo]


class ChainInfo(BaseModel):
    effect: int
    effect_info: EffectInfo

