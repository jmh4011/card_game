from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import WebSocket
from modules.card import Card
from collections import deque
from modules.effect import Effect
from modules.effect_manager import EffectManager
from modules.registry import get_card_instance
from modules.types import ZoneType

import asyncio
import random


class Player:
    def __init__(self, user_id: int,websocket: WebSocket, cards: dict[int, int]) -> None:
        self.user_id = user_id
        self.websocket = websocket
        self.effect_manager = EffectManager()
        self.hands: deque[Card] = deque()
        self.fields: dict[int, Card] = {}
        self.graves: deque[Card] = deque()
        self.decks: deque[Card] = self._initialize_deck(cards)
        self.effect_manager.effects_check(self.decks)

    def _initialize_deck(self, cards: dict[int, int]) -> deque[Card]:
        """Initializes and shuffles the deck with the given card information."""
        deck = deque(
            get_card_instance(card_id=key, zone=ZoneType.DECK, index=0)
            for key, val in cards.items()
            for _ in range(val)
        )
        return self._shuffle(deck)

    def _shuffle(self, cards: deque[Card]) -> deque[Card]:
        """Shuffles the cards and updates their indices."""
        random.shuffle(cards)
        for idx, card in enumerate(cards):
            card.index = idx
        return cards

    def draw(self) -> Card | None:
        """Draws a card from the deck to the hand."""
        if not self.decks:
            return None
        
        card = self.decks.pop()
        self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.HAND)
        card.move(new_zone=ZoneType.HAND, index=len(self.hands))
        self.hands.append(card)
        return card

    def to_field(self, card: Card, index: int) -> None:
        """Moves a card from hand to the field at the specified index."""
        self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.FIELD)
        card.move(new_zone=ZoneType.FIELD, index=index)
        self.fields[index] = card

    def to_grave(self, card: Card) -> None:
        """Moves a card from any zone to the graveyard."""
        self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.GRAVE)
        card.move(new_zone=ZoneType.GRAVE, index=len(self.graves))
        self.graves.append(card)

    def to_deck(self, card: Card, to_top: bool = True, shuffle: bool = False) -> None:
        """Moves a card from any zone to the deck. Optionally shuffles the deck."""
        self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.DECK)

        if to_top:
            self.decks.append(card)
            card.move(new_zone=ZoneType.DECK, index=len(self.decks) - 1)
        else:
            self.decks.appendleft(card)
            card.move(new_zone=ZoneType.DECK, index=0)

        if shuffle:
            self.decks = self._shuffle(self.decks)

    def attact(self, attacker: Card, defender: Card):
        defender.health -= attacker.attack
        if defender.health <= 0:
            return True
        return False