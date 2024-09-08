
from pydantic import BaseModel
from typing import Any, TYPE_CHECKING
from schemas.enum import MoveType, TargetType, ZoneType
from schemas.cards import CardSchemas
if TYPE_CHECKING:
    from modules.card import Card
    from modules.effect import Effect
    from modules.player import Player


    
class ConditionInfo(BaseModel):
    player: 'Player'
    opponent: 'Player'
    trigger_cards: 'Card'
    

class EffectInfo(BaseModel):
    card: 'Card'
    effect: 'Effect'
    targets: list['Card'] = []

class CardInfo(CardSchemas):
    zone: ZoneType
    index: int
    opponent: bool
    before_zone: ZoneType | None = None
    side_effects: list[Any] = []
    effects: list[int]
    
class Target(BaseModel):
    target_id: int
    target_type: TargetType
    zone: ZoneType | None = None  # 카드가 아닌 경우에는 zone이 필요 없을 수 있음
    card: CardInfo | None = None  # 카드가 아닌 경우에도 사용 가능하게 None 허용

class MoveEffect(BaseModel):
    move_id: int
    card: CardInfo
    effect_id: int      
    select: bool
    targets: list[Target]
    tmp: Any

class MoveAttack(BaseModel):
    move_id: int
    select: bool
    card: CardInfo
    targets: list[Target]
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
    

class PlayerInfo(BaseModel):
    cost: int
    health: int
    hands: list['Card']
    fields: dict[int, 'Card'] = {}
    graves: list['Card']
    decks: int

class GameStat(BaseModel):
    Player: PlayerInfo
    opponent: PlayerInfo
    trun: int
    is_player_turn: bool
    
    