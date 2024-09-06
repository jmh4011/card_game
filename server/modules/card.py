from schemas.enum import ZoneType
from schemas.game import CardInfo
from modules.effect import Effect
from schemas.cards import CardSchemas

class Card:
    def __init__(self, card_info: CardSchemas) -> None:
        self.card_id = card_info.card_id
        self.card_name = card_info.card_name
        self.card_class = card_info.card_class
        self.attack = card_info.attack
        self.max_health = card_info.health
        self.health = card_info.health
        self.image_path = card_info.image_path
        self.description = card_info.description
        self.card_type = card_info.card_type
        self.effects = card_info.effects
        self.opponent = False
        self.zone: ZoneType = self.zone
        self.index: int = 0
        self.side_effects = []
        self.before_zone: ZoneType | None = None

    def get_info(self) -> CardInfo:
        return CardInfo(
            card_name=self.card_name,
            card_class=self.card_class,
            description=self.description,
            image_path=self.image_path,
            card_id=self.card_id,
            attack=self.attack,
            health=self.health,
            opponent=self.opponent,
            zone=self.zone,
            index=self.index,
            before_zone=self.before_zone,
            side_effect=self.side_effects,
        )
    
    def move(self, new_zone: ZoneType, index: int):
        self.zone = new_zone
        self.index = index

    # def destroy(self):
        