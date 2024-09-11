from enum import Enum

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