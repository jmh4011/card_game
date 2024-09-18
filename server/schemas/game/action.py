from pydantic import BaseModel
from schemas.game.enums import ActionType
from schemas.game.entity import Entity
from schemas.game.card_info import CardInfo
from schemas.game.player_info import PlayerInfo

class Action(BaseModel):
    action_type: ActionType
    subject: Entity
    object: Entity | None = None
    subject_state: CardInfo | PlayerInfo
    object_state: CardInfo | PlayerInfo | None = None
