from pydantic import BaseModel
from schemas.game.trigger_cards import TriggerCards
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.player import Player

class ConditionInfo(BaseModel):
    player: 'Player'
    opponent: 'Player'
    trigger_cards: TriggerCards
