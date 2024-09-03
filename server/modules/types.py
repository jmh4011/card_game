from enum import Enum
from pydantic import BaseModel
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from modules.card import Card
    from modules.effect import Effect
    from modules.player import Player


class TriggerType(Enum):
    SUMMON = "summon"  # 소환 시
    DESTROY = "destroy"  # 파괴 시
    DRAW = "draw"  # 드로우 시
    MOVE = "move"  # 위치 변경 시
    ATTACK = "attack"  # 공격 시
    DAMAGE = "damage"  # 피해 시
    EFFECT = "effect" #효과 발동 시
    START = "start"  # 시작 시

class TargetType(Enum):
    SELF = "self"  # 이 카드
    PLAYER = "player"  # 내 카드
    OPPONENT = "opponent"  # 상대 카드

class ZoneType(Enum):
    HAND = "hand"
    FIELD = "field"
    GRAVE = "grave"
    DECK = "deck"
    
class ConditionInfo(BaseModel):
    player: 'Player'
    opponent: 'Player'
    trigger_cards: 'Card'
    


class CardInfo(BaseModel):
    card_id: int
    zone: ZoneType
    index: int
    opponent: bool
    attack: int
    health: int
    before_zone: ZoneType | None = None  # 이전 위치, 선택적 필드
    side_effect: list[Any]
    back: bool

class EffectInfo(BaseModel):
    card: 'Card'
    effect: 'Effect'
    targets: list['Card'] = []
    
class MoveType(Enum):
    EFFECT = "effect"
    ATTACT = "attact"
    END = "end"
    
class Targets(BaseModel):
    targer_num: int
    zone: list[ZoneType]
    exception: list[CardInfo]

class Move(BaseModel):
    move_id: int # 행동 번호
    move_type: MoveType # 행동 종류
    select: bool # 강제인지
    card: CardInfo
    targets: Targets
    effect_index: int | None
    tmp: Any
    
class 받는거(BaseModel):
    move_id: int
    target: list[CardInfo]
    tmp: Any