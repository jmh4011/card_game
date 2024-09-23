import asyncio
import logging
import random
from collections import deque
from typing import TYPE_CHECKING

from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from modules.card import Card
from modules.effect_manager import EffectManager
from schemas.game.effect_info import ConditionInfo
from schemas.game.enums import ZoneType
from schemas.game.player_info import PlayerInfo
from schemas.game.trigger_cards import TriggerCards
from schemas.game.entity import Entity
from services import CardServices, DeckServices

if TYPE_CHECKING:
    from modules.effect import Effect

logger = logging.getLogger(__name__)


class Player:
    def __init__(self, user_id: int, websocket: WebSocket, deck_id: int) -> None:
        self.user_id = user_id
        self.websocket = websocket
        self.deck_id = deck_id
        self.effect_manager = EffectManager()
        self.cost = 0
        self.health = 40
        self.hands: deque[Card] = deque()
        self.fields: dict[int, Card] = {}
        self.graves: deque[Card] = deque()
        self.decks: deque[Card] = deque()

    async def start(self, db: AsyncSession) -> None:
        """Initializes and shuffles the deck with the given card information."""
        cards = await DeckServices.get_cards(db=db, deck_id=self.deck_id)
        deck = [
            await self._get_card(card_id=card_id, zone=ZoneType.DECK, db=db)
            for card_id, count in cards.items()
            for _ in range(count)
        ]
        random.shuffle(deck)
        self.decks = deque(deck)
        await self.effect_manager.effects_check(list(self.decks))
        await self.draw(5)

    async def _get_card(self, card_id: int, zone: ZoneType, db: AsyncSession) -> Card:
        db_card = await CardServices.get(card_id=card_id, db=db)
        card = Card(card_info=db_card, player=self, zone=zone)
        await card.initialize_effects(db_card.effects)
        return card

    async def get_info(self) -> PlayerInfo:
        return PlayerInfo(
            cost=self.cost,
            health=self.health,
            hands=[await card.get_info(self) for card in self.hands],
            fields={idx: await card.get_info(self) for idx, card in self.fields.items()},
            graves=[await card.get_info(self) for card in self.graves],
            decks=len(self.decks),
        )

    async def get_available_effects(self, opponent: 'Player', trigger_cards: TriggerCards) -> list['Effect']:
        condition_info = ConditionInfo(
            player=self, opponent=opponent, trigger_cards=trigger_cards
        )
        return await self.effect_manager.get_available_effects(condition_info=condition_info)

    async def entity_to_card(self, entity: Entity, opponent: 'Player') -> Card | None:
        if entity.opponent:
            if entity.zone == ZoneType.HAND:
                if 0 <= entity.index < len(opponent.hands):
                    return opponent.hands[entity.index]
            elif entity.zone == ZoneType.FIELD:
                if entity.index in opponent.fields:
                    return opponent.fields[entity.index]
            elif entity.zone == ZoneType.GRAVE:
                if 0 <= entity.index < len(opponent.graves):
                    return opponent.graves[entity.index]

        else:
            if entity.zone == ZoneType.HAND:
                if 0 <= entity.index < len(self.hands):
                    return self.hands[entity.index]
            elif entity.zone == ZoneType.FIELD:
                if entity.index in self.fields:
                    return self.fields[entity.index]
            elif entity.zone == ZoneType.GRAVE:
                if 0 <= entity.index < len(self.graves):
                    return self.graves[entity.index]
        return None

        
        
    async def draw(self, num: int = 1) -> list[Card]:
        """Draws cards from the deck to the hand."""
        drawn_cards = []
        for _ in range(num):
            if not self.decks:
                break
            card = self.decks.popleft()
            await card.move(new_zone=ZoneType.HAND)
            drawn_cards.append(card)
        return drawn_cards

    async def attack(self, attacker: Card, defender: Card) -> bool:
        """Performs an attack from attacker to defender."""
        defender.health -= attacker.attack
        if defender.health <= 0:
            await defender.move(new_zone=ZoneType.GRAVE)
            return True
        return False

    async def remove_card_from_zone(self, card: Card, zone: ZoneType) -> None:
        """Removes a card from the specified zone."""
        if zone == ZoneType.HAND and card in self.hands:
            self.hands.remove(card)
        elif zone == ZoneType.FIELD and card in self.fields.values():
            index = next((idx for idx, c in self.fields.items() if c == card), None)
            if index is not None:
                del self.fields[index]
        elif zone == ZoneType.GRAVE and card in self.graves:
            self.graves.remove(card)
        elif zone == ZoneType.DECK and card in self.decks:
            self.decks.remove(card)
        else:
            logger.warning(f"Card {card.card_id} not found in zone {zone}.")

    
    async def add_card_to_zone(self, card: Card, zone: ZoneType, index: int | None = None) -> None:
        """Adds a card to the specified zone, optionally at a specific index."""
        if zone == ZoneType.HAND:
            if index is not None and 0 <= index <= len(self.hands):
                self.hands.insert(index, card)  # 지정된 인덱스에 카드 삽입
            else:
                self.hands.append(card)  # 인덱스가 없으면 끝에 추가
        elif zone == ZoneType.FIELD:
            if index is not None:
                self.fields[index] = card  # 필드의 특정 인덱스에 카드 추가
            else:
                # 필드에 빈 자리를 찾아서 추가
                for idx in range(7):  # 필드 슬롯 개수 가정
                    if idx not in self.fields:
                        self.fields[idx] = card
                        break
        elif zone == ZoneType.GRAVE:
            self.graves.append(card)
        elif zone == ZoneType.DECK:
            if index is not None and 0 <= index <= len(self.decks):
                self.decks.insert(index, card)  # 지정된 인덱스에 카드 삽입
            else:
                self.decks.append(card)  # 인덱스가 없으면 끝에 추가
        else:
            logger.warning(f"Unknown zone {zone} for card {card.card_id}.")

    async def shuffle_deck(self) -> None:
        """Shuffles the deck."""
        deck_list = list(self.decks)
        random.shuffle(deck_list)
        self.decks = deque(deck_list)
    
    async def adjust_health(self, amount: int) -> None:
        self.health += amount
        if self.health < 0:
            self.health = 0
        logger.info(f"Player {self.user_id}'s health adjusted by {amount}. New health: {self.health}")

    async def adjust_cost(self, amount: int) -> None:
        self.cost += amount
        if self.cost < 0:
            self.cost = 0
        elif self.cost > 10: 
            self.cost = 10
        logger.info(f"Player {self.user_id}'s cost adjusted by {amount}. New cost: {self.cost}")

    async def set_health(self, new_health: int) -> None:
        self.health = new_health
        if self.health < 0:
            self.health = 0
        logger.info(f"Player {self.user_id}'s health set to {self.health}")

    async def set_cost(self, new_cost: int) -> None:
        self.cost = new_cost
        if self.cost < 0:
            self.cost = 0
        elif self.cost > 10:
            self.cost = 10
        logger.info(f"Player {self.user_id}'s cost set to {self.cost}")
