from enum import Enum


class ZoneType(Enum):
    HAND = "hand"
    FIELD = "field"
    GRAVE = "grave"
    DECK = "deck"

    
    
class MoveType(Enum):
    EFFECT = "effect"
    ATTACK = "attack"
    END = "end"


class TriggerType(Enum):
    SUMMON = "summon"  # 소환 시
    EFFECT = "effect" #효과 발동 시
    DRAW = "draw"  # 드로우 시
    MOVE = "move"  # 위치 변경 시
    ATTACK = "attack"  # 공격 시
    DEFENCE = "defence" # 방어시
    DAMAGE = "damage"  # 피해 시
    DESTROY = "destroy"  # 파괴 시