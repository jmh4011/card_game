from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.player import Player
    from schemas.game.trigger_cards import TriggerCards
    from server.modules.card import Card
    from schemas.game.entity import Entity

class ConditionInfo(BaseModel):
    player: 'Player'
    opponent: 'Player'
    trigger_cards: 'TriggerCards'

class EffectInfo(BaseModel):
    opponent: 'Player'
    target_cards: list['Card']
    targer_enetity: list['Entity']