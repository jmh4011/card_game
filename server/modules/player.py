import asyncio
import logging
import random
from collections import deque
from typing import Dict, List, Optional, TYPE_CHECKING

from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from modules.card import Card
from modules.effect_manager import EffectManager
from schemas.game.condition_info import ConditionInfo
from schemas.game.enums import ZoneType
from schemas.game.player_info import PlayerInfo
from schemas.game.trigger_cards import TriggerCards
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
        self.fields: Dict[int, Card] = {}
        self.graves: deque[Card] = deque()
        self.decks: deque[Card] = deque()

    async def start(self, db: AsyncSession) -> None:
        """Initializes and shuffles the deck with the given card information."""
        cards = await DeckServices.get_cards(db=db, deck_id=self.deck_id)
        deck = [
            await self._get_card(card_id=card_id, zone=ZoneType.DECK, index=idx, db=db)
            for idx, (card_id, count) in enumerate(cards.items())
            for _ in range(count)
        ]
        random.shuffle(deck)
        self.decks = deque(deck)
        await self.effect_manager.effects_check(list(self.decks))
        await self.draw(5)

    async def _get_card(self, card_id: int, zone: ZoneType, index: int, db: AsyncSession) -> Card:
        db_card = await CardServices.get(card_id=card_id, db=db)
        card = Card(card_info=db_card, player=self, zone=zone, index=index)
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

    async def get_available_effects(
        self, opponent: 'Player', trigger_cards: TriggerCards
    ) -> Dict[ZoneType, List['Effect']]:
        condition_info = ConditionInfo(
            player=self, opponent=opponent, trigger_cards=trigger_cards
        )
        return await self.effect_manager.get_available_effects(condition_info=condition_info)

    async def _shuffle(self, cards: deque[Card]) -> None:
        """Shuffles the cards and updates their indices."""
        cards_list = list(cards)
        random.shuffle(cards_list)
        for idx, card in enumerate(cards_list):
            card.index = idx
        cards.clear()
        cards.extend(cards_list)

    async def draw(self, num: int = 1) -> List[Card]:
        """Draws cards from the deck to the hand."""
        drawn_cards = []
        for _ in range(num):
            if not self.decks:
                break
            card = self.decks.popleft()
            await card.move(new_zone=ZoneType.HAND, index=len(self.hands))
            self.hands.append(card)
            await self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.HAND)
            drawn_cards.append(card)
        return drawn_cards

    async def to_field(self, card: Card, index: int) -> None:
        """Moves a card from hand to the field at the specified index."""
        if card in self.hands:
            self.hands.remove(card)
            await card.move(new_zone=ZoneType.FIELD, index=index)
            self.fields[index] = card
            await self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.FIELD)
        else:
            logger.warning(f"Card {card.card_id} not in hand.")

    async def to_grave(self, card: Card) -> None:
        """Moves a card from any zone to the graveyard."""
        await self._remove_card_from_current_zone(card)
        await card.move(new_zone=ZoneType.GRAVE, index=len(self.graves))
        self.graves.append(card)
        await self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.GRAVE)

    async def to_deck(self, card: Card, to_top: bool = True, shuffle: bool = False) -> None:
        """Moves a card from any zone to the deck. Optionally shuffles the deck."""
        await self._remove_card_from_current_zone(card)
        if to_top:
            self.decks.appendleft(card)
            await card.move(new_zone=ZoneType.DECK, index=0)
        else:
            self.decks.append(card)
            await card.move(new_zone=ZoneType.DECK, index=len(self.decks) - 1)
        if shuffle:
            await self._shuffle(self.decks)
        await self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.DECK)

    async def attack(self, attacker: Card, defender: Card) -> bool:
        """Performs an attack from attacker to defender."""
        defender.health -= attacker.attack
        if defender.health <= 0:
            await defender.player.to_grave(defender)
            return True
        return False

    async def _remove_card_from_current_zone(self, card: Card) -> None:
        """Removes a card from its current zone."""
        if card.zone == ZoneType.HAND and card in self.hands:
            self.hands.remove(card)
        elif card.zone == ZoneType.FIELD and card in self.fields.values():
            index = list(self.fields.keys())[list(self.fields.values()).index(card)]
            del self.fields[index]
        elif card.zone == ZoneType.GRAVE and card in self.graves:
            self.graves.remove(card)
        elif card.zone == ZoneType.DECK and card in self.decks:
            self.decks.remove(card)
        else:
            logger.warning(f"Card {card.card_id} not found in current zone {card.zone}.")
