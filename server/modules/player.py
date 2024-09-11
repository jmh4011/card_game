from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import WebSocket
from modules.card import Card
from collections import deque
from modules.effect import Effect
from modules.effect_manager import EffectManager
from modules.registry import get_effect
from schemas.game.enums import ZoneType
from schemas.game.games import PlayerInfo
from services import DeckServices, CardServices
from crud import DeckCardCrud
import logging
import asyncio
import random

logger = logging.Logger(__name__)

class Player:
    def __init__(self, user_id: int, websocket: WebSocket, deck_id:int) -> None:
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

    async def start(self, db:AsyncSession) -> deque[Card]:
        """Initializes and shuffles the deck with the given card information."""
        cards = await DeckServices.get_cards(db=db, deck_id=self.deck_id)
        deck = [await self._get_card(card_id=key,zone=ZoneType.DECK,index=idx , db=db)
            for idx,(key,val) in enumerate(cards.items())
            for _ in range(val)]
        logger.warning(deck)
        self.decks = deque(deck)
        await self.effect_manager.effects_check(self.decks)
        await self.draw(5)
    
    async def _get_card(self, card_id:int, zone:ZoneType, index:int,db:AsyncSession):
        db_card = await CardServices.get(card_id=card_id,db=db)
        card = Card(card_info=db_card, player=self, zone=zone, index=index)
        await card.initialize_effects(db_card.effects)
        return card
    
    async def get_info(self) -> PlayerInfo:
        return PlayerInfo(
            cost=self.cost,
            health=self.health,
            hands=[await card.get_info(self) for card in self.hands],
            fields={idx:await card.get_info(self) for idx,card in self.fields.items()},
            graves=[await card.get_info(self) for card in self.graves],
            decks=len(self.decks)
        )

    async def _shuffle(self, cards: deque[Card]) -> deque[Card]:
        """Shuffles the cards and updates their indices."""
        random.shuffle(cards)
        for idx, card in enumerate(cards):
            card.index = idx
        return cards

    async def draw(self, num = 1) -> list[Card]:
        """Draws a card from the deck to the hand."""
        result = []
        for _ in range(num):
            if not self.decks:
                break
            
            card = self.decks.pop()
            await self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.HAND)
            await card.move(new_zone=ZoneType.HAND, index=len(self.hands))
            self.hands.append(card)
            result.append(card)
        return result

    async def to_field(self, card: Card, index: int) -> None:
        """Moves a card from hand to the field at the specified index."""
        await self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.FIELD)
        await card.move(new_zone=ZoneType.FIELD, index=index)
        self.fields[index] = card

    async def to_grave(self, card: Card) -> None:
        """Moves a card from any zone to the graveyard."""
        await self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.GRAVE)
        await card.move(new_zone=ZoneType.GRAVE, index=len(self.graves))
        self.graves.append(card)

    async def to_deck(self, card: Card, to_top: bool = True, shuffle: bool = False) -> None:
        """Moves a card from any zone to the deck. Optionally shuffles the deck."""
        await self.effect_manager.on_card_moved(card=card, new_zone=ZoneType.DECK)

        if to_top:
            self.decks.append(card)
            await card.move(new_zone=ZoneType.DECK, index=len(self.decks) - 1)
        else:
            self.decks.appendleft(card)
            await card.move(new_zone=ZoneType.DECK, index=0)

        if shuffle:
            self.decks = self._shuffle(self.decks)

    async def attact(self, attacker: Card, defender: Card):
        defender.health -= attacker.attack
        if defender.health <= 0:
            return True
        return False