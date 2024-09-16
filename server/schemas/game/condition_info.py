from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.player import Player
    from schemas.game.trigger_cards import TriggerCards

class ConditionInfo(BaseModel):
    player: 'Player'
    opponent: 'Player'
    trigger_cards: 'TriggerCards'
