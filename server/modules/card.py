import asyncio
from typing import TYPE_CHECKING
from schemas.game.enums import ZoneType
from modules.effect import Effect
from schemas.db.cards import CardSchemas
from modules.registry import get_effect
from schemas.game.card_info import CardInfo
if TYPE_CHECKING:
    from modules.player import Player

class Card:
    def __init__(self, card_info: CardSchemas, player: 'Player', zone: ZoneType, index: int) -> None:
        self.card_id = card_info.card_id
        self.card_name = card_info.card_name
        self.card_class = card_info.card_class
        self.attack = card_info.attack
        self.max_health = card_info.health
        self.health = card_info.health
        self.image_path = card_info.image_path
        self.card_type = card_info.card_type
        self.player = player
        self.zone: ZoneType = zone
        self.index: int = index
        self.side_effects = []
        self.before_zone: ZoneType | None = None
        self.effects: list[Effect] = [] 

    async def initialize_effects(self, effects_info: list[int]) -> None:
        """비동기 작업을 통해 효과를 초기화하는 메서드"""
        results = await asyncio.gather(*[get_effect(i) for i in effects_info])
        self.effects = [effect(self) for effect in results]
        

    async def get_info(self, player: 'Player') -> 'CardInfo':
        return CardInfo(
            card_name=self.card_name,
            card_class=self.card_class,
            image_path=self.image_path,
            card_id=self.card_id,
            attack=self.attack,
            health=self.health,
            opponent=self.player != player,
            zone=self.zone,
            index=self.index,
            before_zone=self.before_zone,
            side_effect=self.side_effects,
            card_type=self.card_type,
            effects=[i.effect_id for i in self.effects]
        )
    
    async def move(self, new_zone: ZoneType, index: int):
        self.zone = new_zone
        self.index = index

    # def destroy(self):
        