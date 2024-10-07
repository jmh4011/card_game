from pydantic import BaseModel
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from modules.player import Player
    from schemas.game.trigger_cards import TriggerCards
    from server.modules.card import Card
    from schemas.game.entity import Entity
    from modules.effect import Effect

class ConditionInfo(BaseModel):
    player: 'Player'
    opponent: 'Player'
    trigger_cards: 'TriggerCards'

class TargetInfo(BaseModel):
    entity: 'Entity'
    card: 'Card' | None

class EffectInfo(BaseModel):
    opponent: 'Player'
    targets: list[TargetInfo]
    
class ChainInfo(BaseModel):
    effect: 'Effect'
    effect_info: 'EffectInfo'