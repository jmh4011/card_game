from schemas.enum import ZoneType
from modules.card import Card
from modules.cards import *

# card id와 자식 클래스의 매핑
CARD_CLASS_MAP: dict[int, type[Card]] = {
    1: Card_1,
    2: Card_2,
    3: Card_3,
}

def get_card_instance(card_id:int, zone: ZoneType, index: int, before_zone: ZoneType | None = None):
    return CARD_CLASS_MAP.get(card_id)(zone=zone, index=index, before_zone=before_zone)
