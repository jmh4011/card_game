import asyncio
import logging
from typing import TYPE_CHECKING

from schemas.db.cards import CardSchemas
from schemas.game.class_info import CardInfo
from schemas.game.enums import ZoneType

if TYPE_CHECKING:
    from modules.effect import Effect
    from modules.player import Player
    from modules.game_manager import GameManager


logger = logging.getLogger(__name__)

class Card:
    async def __init__(
        self,game_manager: 'GameManager',card_info: CardSchemas, player_id: int, zone: ZoneType, instance_id: int
    ) -> None:
        self.game_manager: 'GameManager' = game_manager
        self.instance_id: int = instance_id
        self.card_id: int = card_info.card_id
        self.card_name: str = card_info.card_name
        self.card_class: str = card_info.card_class
        self.attack: int = card_info.attack
        self.max_health: int = card_info.health
        self.health: int = card_info.health
        self.image_path: str = card_info.image_path
        self.card_type: str = card_info.card_type
        self.player_id: int = player_id
        self.zone: ZoneType = zone
        self.before_zone: ZoneType | None = None
        self.effects: list[int] = self._initialize_effects(card_info.effects)
        self.side_effects: list[int] = []

    async def _initialize_effects(self, effects_info: list[int]) -> list[int]:
        effects = await asyncio.gather(*[self.game_manager.registry_manager.create_effect_instance(effect_id,self.instance_id) 
                                                for effect_id in effects_info])
        return effects

    async def _get_info(self) -> CardInfo:
        return CardInfo(
            card_name = self.card_name,
            card_class = self.card_class,
            image_path = self.image_path,
            card_id = self.card_id,
            attack = self.attack,
            health = self.health,
            card_type = self.card_type,
            effects = self.effects,
        )
    
    async def _is_public_player(self) -> bool:
        if self.zone == ZoneType.DECK:
            return False
        return True
        
    
    async def _is_public_opponet(self) -> bool:
        if self.zone == ZoneType.HAND:
            return False
        elif self.zone == ZoneType.DECK:
            return False
        elif self.zone == ZoneType.FIELD:
            return True
        elif self.zone == ZoneType.GRAVE:
            return True
        else:
            return None

    async def is_public(self,player_id:int) -> bool:
        if (player_id == self.player_id and await self._is_public_player()) or await self._is_public_opponet():
            return True
        return False
    
    
    async def get_info(self, player_id:int):
        if self.is_public(player_id=player_id):
            return await self._get_info()
        return None

    async def move(self, new_zone: ZoneType) -> None:
        self.before_zone = self.zone
        self.zone = new_zone