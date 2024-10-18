import logging
import random
from typing import TYPE_CHECKING

from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from modules.effect_manager import EffectManager
from schemas.game.enums import ZoneType
from schemas.game.class_info import PlayerInfo
from services import DeckServices

if TYPE_CHECKING:
    from schemas.game.effect_info import ConditionInfo
    from modules.game_manager import GameManager
    from modules.game_manager import GameManager
logger = logging.getLogger(__name__)


class Player:
    def __init__(self, game_manager: 'GameManager',user_id: int, player_id:int,websocket: WebSocket, deck_id: int) -> None:
        self.game_manager = game_manager
        self.user_id = user_id
        self.player_id = player_id
        self.websocket = websocket
        self.deck_id = deck_id
        self.effect_manager = EffectManager()
        self.cost = 0
        self.max_cost = 0
        self.health = 40
        self.max_health = 40
        self.hands: list[int] = []
        self.fields: dict[int, int] = {}
        self.graves: list[int] = []
        self.decks: list[int] = []
        self.effects: list[int] = []
        self.side_effects: list[int] = []

    async def start(self, db: AsyncSession) -> None:
        """Initializes and shuffles the deck with the given card information."""
        cards = await DeckServices.get_cards(db=db, deck_id=self.deck_id)
        deck = [
            await self.game_manager.registry_manager.create_card_instance(card_id=card_id, zone=ZoneType.DECK,player_id=self.user_id)
            for card_id, count in cards.items()
            for _ in range(count)
        ]
        random.shuffle(deck)
        self.decks = deck
        await self.effect_manager.effects_check(self.decks)
        await self.draw(5)


    async def _get_info(self) -> PlayerInfo:
        return PlayerInfo(
            cost=self.cost,
            health=self.health,
            hands=[(await self.game_manager.registry_manager.get_card_instance(card)).get_info_player() 
                    for card in self.hands],
            fields={idx: (await self.game_manager.registry_manager.get_card_instance(card)).get_info_player() 
                    for idx, card in self.fields.items()},
            graves=[(await self.game_manager.registry_manager.get_card_instance(card)).get_info_player()
                    for card in self.graves],
            decks=len(self.decks),
            effects=self.effects,
            side_effects=self.side_effects
        )
    
    async def get_info_player(self):
        return await self._get_info()
    
    async def get_info_opponent(self):
        return await self._get_info()

    async def get_available_effects(self, condition_info:'ConditionInfo'):
        return await self.effect_manager.get_available_effects(condition_info=condition_info)


    async def remove_card(self, card_id: int, zone: ZoneType) -> int | None:
        index = None
        
        if zone == ZoneType.HAND and card_id in self.hands:
            index = self.hands.index(card_id)
            del self.hands[index]
        elif zone == ZoneType.FIELD and card_id in self.fields.values():
            index = next((idx for idx, c in self.fields.items() if c == card_id), None)
            if index is not None:
                del self.fields[index]
        elif zone == ZoneType.GRAVE and card_id in self.graves:
            index = self.graves.index(card_id)
            del self.graves[index]
        elif zone == ZoneType.DECK and card_id in self.decks:
            index = self.decks.index(card_id)
            del self.decks[index]
        else:
            logger.warning(f"Card {card_id} not found in zone {zone}.")
        
        return index


    
    async def add_card_to_zone(self, card_id: int, zone: ZoneType, index: int | None = None) -> None:
        """Adds a card to the specified zone, optionally at a specific index."""
        if zone == ZoneType.HAND:
            if index is not None and 0 <= index <= len(self.hands):
                self.hands.insert(index, card_id)  # 지정된 인덱스에 카드 삽입
            else:
                self.hands.append(card_id)  # 인덱스가 없으면 끝에 추가
        elif zone == ZoneType.FIELD:
            if index is not None:
                self.fields[index] = card_id  # 필드의 특정 인덱스에 카드 추가
            else:
                # 필드에 빈 자리를 찾아서 추가
                for idx in range(5):  # 필드 슬롯 개수 가정
                    if idx not in self.fields:
                        self.fields[idx] = card_id
                        break
        elif zone == ZoneType.GRAVE:
            if index is not None and 0 <= index <= len(self.graves):
                self.graves.insert(index, card_id)  # 지정된 인덱스에 카드 삽입
            else:
                self.graves.append(card_id)  # 인덱스가 없으면 끝에 추가
        elif zone == ZoneType.DECK:
            if index is not None and 0 <= index <= len(self.decks):
                self.decks.insert(index, card_id)  # 지정된 인덱스에 카드 삽입
            else:
                self.decks.append(card_id)  # 인덱스가 없으면 끝에 추가
        else:
            logger.warning(f"Unknown zone {zone} for card {card_id}.")


    async def shuffle_deck(self) -> None:
        """Shuffles the deck."""
        deck_list = self.decks
        random.shuffle(deck_list)
        self.decks = deck_list
    
