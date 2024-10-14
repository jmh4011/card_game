from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING, Union

from schemas.game.enums import TriggerType
from modules.player import Player
from modules.card import Card
from schemas.game.entity import Entity
from modules.effect import Effect

class ConditionInfo(BaseModel):
    player: Player
    opponent: Player
    trigger_cards: dict[TriggerType, list[Card]]

    # Pydantic v2에서의 모델 설정
    model_config = ConfigDict(arbitrary_types_allowed=True)

class TargetInfo(BaseModel):
    entity: Entity
    card: Union[Card, None]

    model_config = ConfigDict(arbitrary_types_allowed=True)

class EffectInfo(BaseModel):
    opponent: Player
    targets: list[TargetInfo]

    model_config = ConfigDict(arbitrary_types_allowed=True)

class ChainInfo(BaseModel):
    effect: Effect
    effect_info: EffectInfo

    model_config = ConfigDict(arbitrary_types_allowed=True)
