from typing import Any
from pydantic import BaseModel
from schemas.game.enums import ActionType
from schemas.game.entity import Entity
from schemas.game.card_info import CardInfo


class Action(BaseModel):
    action_type: ActionType
    action_data: Any

class ActionMove(BaseModel):
    before: Entity
    after: Entity

class ActionCardState(BaseModel):
    entity: Entity
    state: CardInfo

class ActionSideEffect(BaseModel):
    entity: Entity
    effect: int

class ActionCost(BaseModel):
    cost: int

class ActionEffect(BaseModel):
    effect: int
    subject: Entity
    targets: list[Entity] = []

class ActionAtteck(BaseModel):
    subject: Entity
    object: Entity

class ActionDestroy(BaseModel):
    before: Entity
    after: Entity

class ActionDamage(BaseModel):
    entity: Entity
    damage: int
