from fastapi import WebSocket
from modules.effect import Effect
from modules.effects import *
from modules.card import Card
from modules.player import Player
from schemas.game.enums import ZoneType
from services.cards import CardServices
from services.users import UserServices
from sqlalchemy.ext.asyncio import AsyncSession



class RegistryManager:
    EFFECT_DICT: dict[int, type[Effect]] = {
        1: Effect_1,
        2: Effect_2,
    }
    def __init__(self, 
                db: AsyncSession, 
                mod_id:int):
        
        self.db = db
        self.mod_id = mod_id
        
        self.card_instance_id_counter = 1
        self.effect_instance_id_counter = 1
        self._card_registry: dict[int, Card] = {}
        self._player_registry: dict[int, Player] = {}
        self._effect_registry: dict[int, Effect] = {}
    
    @classmethod
    async def get_effect(cls,effect_id:int):
        return cls.EFFECT_DICT.get(effect_id)

    async def create_card_instance(self, card_id: int, player_id:int, zone:ZoneType) -> int:
        db_card = await CardServices.get(card_id=card_id, db=self.db)   
        card = Card(
            game_manager=self,
            player_id=player_id,
            card_info=db_card,
            zone=zone,
            instance_id=self.card_instance_id_counter)
        self._card_registry[self.card_instance_id_counter] = card
        self.card_instance_id_counter += 1
        return card
    
    async def create_player_instance(self, player_id: int,user_id:int, websocket:WebSocket) -> int:
        player_deck = await UserServices.get_deck_selection(db=self.db, user_id=user_id, mod_id=self.mod_id)
        player = Player(player_id=player_id,
                        user_id=user_id,
                        websocket=websocket,
                        deck_id=player_deck.deck_id,
                        game_manager=self)
        self._player_registry[player_id] = player
        return player
    
    async def create_effect_instance(self, effect_id: int, card_id: int) -> int:
        effect_class = await self.get_effect(effect_id)
        effect = effect_class(game_manager=self,
                                instance_id=self.effect_instance_id_counter,
                                card_id=card_id)
        self._effect_registry[self.effect_instance_id_counter] = effect
        self.effect_instance_id_counter += 1
        return effect
    
    async def get_card_instance(self,id: int) -> 'Card':
        return self._card_registry[id]
        
    async def get_player_instance(self,id: int) -> 'Player':
        return self._player_registry[id]

    async def get_effect_instance(self,id: int) -> 'Effect':
        return self._effect_registry[id]
    
    
    async def get_opponent_id(self,player_id) -> int:
        return 1 if player_id == 2 else 2
    
    async def get_opponent_instance(self,player_id) -> 'Player':
        return await self.get_player_instance(1 if player_id == 2 else 2)