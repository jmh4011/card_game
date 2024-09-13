from enum import Enum

class MessageType(Enum):
    PING = "ping"
    TEXT = "text"
    GAMEINFO = "gameinfo"
    ACRION = "action"
    MOVE = "move"

class MessageReturnType(Enum):
    TEXT = "text"
    MOVE = "move"
    CANCEL = "cancel"
    END = "end"


class ZoneType(Enum):
    HAND = "hand"
    FIELD = "field"
    GRAVE = "grave"
    DECK = "deck"

class ActionType(Enum):
    DROW = "drow"
    ATTACK = "attack"
    DESTROY = "destroy"
    MOVE = "move"
    SUMMON = "summon"
    DAMAGE = "damege"
    EFFECT = "effect"
    
    
class MoveType(Enum):
    EFFECT = "effect"
    ATTACT = "attact"
    END = "end"

class EntityZoneType(Enum):
    HAND = "hand"
    FIELD = "field"
    GRAVE = "grave"
    DECK = "deck"
    PLAYER = 'player'

class TriggerType(Enum):
    SUMMON = "summon"  # 소환 시
    EFFECT = "effect" #효과 발동 시
    DRAW = "draw"  # 드로우 시
    MOVE = "move"  # 위치 변경 시
    ATTACK = "attack"  # 공격 시
    DEFENCE = "defence" # 방어시
    DAMAGE = "damage"  # 피해 시
    DESTROY = "destroy"  # 파괴 시