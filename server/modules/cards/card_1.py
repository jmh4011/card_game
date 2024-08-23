from modules.card import Card
from modules.types import ZoneType
from modules.effects import *


class Card_1(Card):
    def __init__(self, zone: ZoneType, index: int, before_zone: ZoneType | None = None):
        super().__init__(
            card_id=1,
            card_name="Test Card 1",
            card_class="Type A",
            attack=1,
            max_health=1,
            health=1,
            description="This is a test card",
            card_type=0,
            side_effects=[],
            effects=[Effect_1],  # 예시 효과 ID
            zone=zone,
            index=index,
            before_zone=before_zone
        )