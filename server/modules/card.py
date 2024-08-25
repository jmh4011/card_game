from modules.types import ZoneType, CardInfo
from modules.effect import Effect

class Card:
    def __init__(self, card_id: int, card_name: str, card_class: str, attack: int, max_health: int,
                health: int, description: str, card_type: int, side_effects: list, effects: list[Effect],
                zone: ZoneType, index: int, before_zone: ZoneType | None = None) -> None:
        self.card_id = card_id
        self.card_name = card_name
        self.card_class = card_class
        self.attack = attack
        self.max_health = max_health
        self.health = health
        self.description = description
        self.card_type = card_type
        self.side_effects = side_effects
        self.effects = effects
        
        self.zone: ZoneType = zone
        self.index: int = index
        self.before_zone: ZoneType | None = before_zone

    def get_info(self) -> CardInfo:
        return CardInfo(
            card_id=self.card_id,
            attack=self.attack,
            health=self.health,
            opponent=False,
            zone=self.zone,
            index=self.index,
            before_zone=self.before_zone,
            side_effect=self.side_effects,
            back=False
        )
    
    def move(self, new_zone: ZoneType, index: int):
        self.zone = new_zone
        self.index = index

    # def destroy(self):
        