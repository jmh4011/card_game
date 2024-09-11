
from pydantic import BaseModel
from typing import Any, TYPE_CHECKING
from schemas.game.enums import MoveType, ActionType, EntityZoneType, ZoneType
from schemas.db.cards import CardSchemas
if TYPE_CHECKING:
    from modules.card import Card
    from modules.effect import Effect
    from modules.player import Player


class Entity(BaseModel):
    zone: EntityZoneType
    index: int
    opponent: bool
    class Config:
        use_enum_values = True

class ConditionInfo(BaseModel):
    player: 'Player'
    opponent: 'Player'
    trigger_cards: 'Card'
    

class CardInfo(CardSchemas):
    zone: ZoneType
    index: int
    opponent: bool
    side_effects: list[Any] = []
    effects: list[int]
    class Config:
        use_enum_values = True
    
class MoveEffect(BaseModel):
    move_id: int
    entity: Entity
    effect_id: int      
    select: bool
    targets: list[Entity]
    tmp: Any

class MoveAttack(BaseModel):
    move_id: int
    entity: Entity
    select: bool
    targets: list[Entity]
    tmp: Any
    
class Move(BaseModel):
    effects: list[MoveEffect] = []
    attact: list[MoveAttack] = []
    end: bool
    
    
class MoveReturn(BaseModel):
    move_type: MoveType
    move_id: int
    target: list[int]
    tmp: Any
    class Config:
        use_enum_values = True

class PlayerInfo(BaseModel):
    cost: int
    health: int
    hands: list[CardInfo]
    fields: dict[int, CardInfo] = {}
    graves: list[CardInfo]
    decks: int

class GameStat(BaseModel):
    Player: PlayerInfo
    opponent: PlayerInfo
    trun: int
    is_player_turn: bool
    class Config:
        use_enum_values = True


class Action(BaseModel):
    action_type: ActionType
    subject: Entity  
    object: Entity
    subject_state: CardInfo | PlayerInfo
    object_state: CardInfo | PlayerInfo