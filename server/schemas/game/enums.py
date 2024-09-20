from enum import Enum

class MessageType(Enum):
    PING = "ping"
    TEXT = "text"
    GAME_INFO = "game_info"
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
    MOVE = "move"
    CARD_STATE = "card_state"
    SIDE_EFFECT = "side_effect"
    COST = "cost"
    ATTACK = "attack"
    DESTROY = "destroy"
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