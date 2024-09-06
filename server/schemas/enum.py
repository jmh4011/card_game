from enum import Enum

class TriggerType(Enum):
    SUMMON = "summon"  # 소환 시
    DESTROY = "destroy"  # 파괴 시
    DRAW = "draw"  # 드로우 시
    MOVE = "move"  # 위치 변경 시
    ATTACK = "attack"  # 공격 시
    DAMAGE = "damage"  # 피해 시
    EFFECT = "effect" #효과 발동 시
    START = "start"  # 시작 시


class ZoneType(Enum):
    HAND = "hand"
    FIELD = "field"
    GRAVE = "grave"
    DECK = "deck"
    
    
    
class MoveType(Enum):
    EFFECT = "effect"
    ATTACT = "attact"
    END = "end"


class TargetType(Enum):
    SELF = "self"  # 이 카드
    PLAYER = "player"  # 플레이어 (내)
    OPPONENT_PLAYER = "opponent_player"  # 상대 플레이어
    CARD = "card"  # 카드 (내)
    OPPONENT_CARD = "opponent_card"  # 상대 카드