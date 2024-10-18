from enum import Enum
from typing import Any
from pydantic import BaseModel
from schemas.game.enums import ZoneType
from schemas.game.entity import Entity
from schemas.game.class_info import CardInfo

class ActionType(Enum):
    MOVE = "move"
    SET_CARD = "set_card"
    SET_PLAYER = "set_player"
    SET_GAME = "set_game"
    ATTACK = "attack"
    DAMAGE = "damege"
    EFFECT = "effect"

class SetCardType(Enum):
    NAME = "name"
    CLASS = "class"
    ATTACK = "attack"
    HEALTH = "health"
    IMAHE_PATH = "image_path"
    TYPE = "type"
    EFEECTS = "effects"
    
class SetPlayerType(Enum):
    COST = "cost"
    ATTACK = "attack"
    HEALTH = "health"
    EFEECTS = "effects"

class SetGameType(Enum):
    EFEECTS = "effects"

class Action(BaseModel):
    action_type: ActionType
    action_data: Any

class ActionSetCard(BaseModel):
    card: Entity
    type: SetCardType
    data: Any

class ActionSetPlayer(BaseModel):
    opponent: bool
    type: SetPlayerType
    data: Any

class ActionSetGame(BaseModel):
    type: SetGameType
    data: Any


class ActionMove(BaseModel):
    before: Entity | None
    after: Entity
    destroy: bool = False
    state: CardInfo | None
    

class ActionEffect(BaseModel):
    effect_id: int
    entity: Entity
    targets: list[Entity] = []

class ActionAtteck(BaseModel):
    subject: Entity
    object: Entity

class ActionDamage(BaseModel):
    entity: Entity
    damage: int