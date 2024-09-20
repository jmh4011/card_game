import asyncio
from typing import TYPE_CHECKING

from modules.registry import get_effect
from schemas.db.cards import CardSchemas
from schemas.game.card_info import CardInfo
from schemas.game.enums import ZoneType

if TYPE_CHECKING:
    from modules.effect import Effect
    from modules.player import Player


class Card:
    def __init__(
        self, card_info: CardSchemas, player: 'Player', zone: ZoneType
    ) -> None:
        self.card_id: int = card_info.card_id
        self.card_name: str = card_info.card_name
        self.card_class: str = card_info.card_class
        self.attack: int = card_info.attack
        self.max_health: int = card_info.health
        self.health: int = card_info.health
        self.image_path: str = card_info.image_path
        self.card_type: str = card_info.card_type
        self.player: 'Player' = player
        self.zone: ZoneType = zone
        self.side_effects: list['Effect'] = []
        self.before_zone: ZoneType | None = None
        self.effects: list['Effect'] = []

    async def initialize_effects(self, effects_info: list[int]) -> None:
        """Initializes effects asynchronously."""
        effect_classes = await asyncio.gather(*[get_effect(effect_id) for effect_id in effects_info])
        self.effects = [effect_class(self) for effect_class in effect_classes]

    async def get_info(self, player: 'Player') -> CardInfo:
        return CardInfo(
            card_name=self.card_name,
            card_class=self.card_class,
            image_path=self.image_path,
            card_id=self.card_id,
            attack=self.attack,
            health=self.health,
            side_effect=self.side_effects,
            card_type=self.card_type,
            effects=[effect.effect_id for effect in self.effects],
        )

    async def move(self, new_zone: ZoneType, index: int | None = None) -> None:
        """Moves the card to a new zone and updates the player's card collections."""
        self.before_zone = self.zone
        self.zone = new_zone

        # 이전 존에서 카드 제거
        if self.before_zone:
            await self.player.remove_card_from_zone(self, self.before_zone)

        # 새로운 존에 카드 추가
        await self.player.add_card_to_zone(self, new_zone, index)

        # 카드 이동에 따른 효과 처리
        await self.player.effect_manager.on_card_moved(card=self, new_zone=new_zone)
