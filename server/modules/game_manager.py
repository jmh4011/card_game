# modules/game_manager.py

import asyncio
import random
import logging

from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from modules.player import Player
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.game.enums import MoveType, ZoneType
from modules.effect import Effect
from schemas.game.message import MessageModel, MessageReturnModel, MessageReturnType, MessageType
from schemas.game.move import Move, MoveReturn
from schemas.game.trigger_cards import TriggerCards
from schemas.game.effect_info import ChainInfo, ConditionInfo, EffectInfo
from schemas.game.entity import Entity
from modules.registry_manager import RegistryManager
from schemas.game.action import Action, ActionType
from schemas.game.class_info import GameInfo
from modules.card import Card
from server.modules.action_manager import ActionManager

logger = logging.getLogger(__name__)

class GameManager:
    async def __init__(self, 
                db: AsyncSession, 
                mod_id:int,
                user1_id: int, 
                user2_id: int,
                user1_websocket:WebSocket,
                user2_websocket:WebSocket):
        self.db = db
        self.mod_id = mod_id
        self.active = True
        self.turn = 0
        self.trigger_cards:TriggerCards = TriggerCards()
        self.effects: list[int] = []
        self.side_effects: list[int] = []
        self._game_over_event = asyncio.Event()
        
        self.registry_manager = RegistryManager()
        self.action_manager = ActionManager()
        await self.registry_manager.create_player_instance(player_id=1,
                                                        user_id=user1_id,
                                                        websocket=user1_websocket),
            
        await self.registry_manager.create_player_instance(player_id=2,
                                                        user_id=user2_id,
                                                        websocket=user2_websocket),
        
    async def wait_until_game_over(self):
        await self._game_over_event.wait()
    
    async def _send_message(self, player_id: int, message_type: MessageType, data):
        try:
            player = await self.registry_manager.get_player_instance(player_id)
            if player.websocket.client_state == WebSocketState.CONNECTED:
                message = MessageModel(type=message_type, data=data).model_dump()
                await player.websocket.send_json(message)
                logger.info(f"Sent message to player {player.user_id}: {message_type}")
            else:
                logger.warning(f"WebSocket not connected for player {player.user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to player {player.user_id}: {e}")


    async def receive_message(self, player_id: int, timeout=30.0) -> MessageReturnModel | None:
        
        player = await self.registry_manager.get_player_instance(player_id)
        while True:
            try:
                logger.info(f"Waiting for message from Player {player.user_id}")
                message_text = await asyncio.wait_for(player.websocket.receive_text(), timeout=timeout)
                try:
                    message = MessageReturnModel.model_validate_json(message_text)
                    logger.info(f"{player.user_id}: {message}")
                    return message
                except Exception as e:
                    logger.warning(f"{player.user_id}: {message_text}")
            except asyncio.TimeoutError:
                logger.warning(f"Player {player.user_id}가 {timeout}초 내에 응답하지 않았습니다.")
                if not await self.check_connection(player):
                    logger.warning(f"Player {player.user_id}의 연결이 끊어졌습니다.")
                    await self.handle_disconnect(player)
                else:
                    logger.warning(f"Player {player.user_id}의 연결은 유지되고 있습니다.")
                return None
            except Exception as e:
                logger.error(f"Error in receiving message from Player {player.user_id}: {e}")
                raise e

    async def check_connection(self, player_id: int) -> bool:
        try:
            # 연결 상태를 확인하기 위해 작은 메시지를 보냅니다
            await self._send_message(player_id=player_id, message_type=MessageType.PING, data=None)
            return True
        except Exception as e:
            logger.error(f"Connection check failed for Player {player_id}: {e}")
            return False

    async def game_start(self):
        try:
            if random.randint(0, 1):
                turn_player_id = 1
                not_turn_player_id = 2
            else:
                turn_player_id = 2
                not_turn_player_id = 1
            turn_player = await self.registry_manager.get_player_instance(turn_player_id)
            await turn_player.start(self.db)
            not_turn_player = await self.registry_manager.get_player_instance(not_turn_player_id)
            await not_turn_player.start(self.db)
            await self.send_game_stat(turn_player_id)
            await self.send_game_stat(not_turn_player_id)
            await self.handle_turn(turn_player_id, not_turn_player_id)
        except Exception as e:
            logger.error(f"Error in game start: {e}")
        finally:
            logger.error(f"게임 종료")
            await self.stop()
            # 게임 종료 이벤트 설정
            self._game_over_event.set()

    async def send_game_stat(self, player_id:int):
        player = await self.registry_manager.get_player_instance(player_id)
        opponent = await self.registry_manager.get_opponent_instance(player_id)
        player_info = await player.get_info_player()
        opponent_info = await opponent.get_info_opponent()

        game_stat = GameInfo(
            player=player_info,
            opponent=opponent_info,
            turn=self.turn,
            is_player_turn=True,
            effects=self.effects
        )
        await self._send_message(player_id, MessageType.GAME_INFO, game_stat)


    async def handle_turn(self,first_player_id:int, other_player_id: int):
        turn_player_id = first_player_id
        not_turn_player_id = other_player_id
        while self.active:
            logger.info(f"Player {turn_player_id}'s turn.")
            while True:
                if await self.handle_chain(turn_player_id,not_turn_player_id):
                    break
            turn_player_id, not_turn_player_id = not_turn_player_id, turn_player_id
            self.turn += 1
            await self.send_game_stat()
        logger.info("게임이 종료되었습니다.")


    async def handle_chain(self,first_player_id:int, other_player_id: int):
        
        move_player_id = first_player_id
        not_move_player_id = other_player_id
        add_chain = True
        chain_effects: list[ChainInfo] = []
        while True:
            logger.info(f"Player {move_player_id}'s move.")
            available_effects = await self.send_available_move()
            message = await self.receive_message(move_player_id)
            if message is None:
                break  # 연결이 끊어졌을 경우 루프 종료
            if message.type == MessageReturnType.MOVE:
                result = await self.handle_move(message.data,available_effects)
                if result:
                    chain_effects.append(result) 
                    move_player_id, not_move_player_id = not_move_player_id, move_player_id
                    add_chain = True
            elif message.type == MessageReturnType.CANCEL:
                if await self.handle_cancel(move_player_id):
                    move_player_id, not_move_player_id = not_move_player_id, move_player_id
                    if add_chain:
                        add_chain = False
                    else:
                        break
            else:
                logger.info(f"Player {move_player_id}: {message.data}")
                # 필요에 따라 추가 처리
        
        if chain_effects == []:
            return True
        
        for chain_info in chain_effects:
            effect = await self.registry_manager.get_effect_instance(chain_info.effect_id)
            effect.after(effect_info=chain_info.effect_info)
        return False


    async def handle_move(self, player_id:int, data: MoveReturn, available_effects: list[Effect] ):
        logger.info(f"Processing move from Player {player_id}: {data}")
        effect = available_effects[data.move_index]
        effect_info = EffectInfo(player_id=player_id,
                                targets=[effect.targets[idx] for idx in data.target])
        effect.before(effect_info=effect_info)
        
        return ChainInfo(effect=effect,effect_info=effect_info)
        

    async def handle_cancel(self,player_id:int):
        logger.info(f"Player {player_id}: cancel")
        return True
        
        
    async def handle_disconnect(self, player_id: int):
        """플레이어의 연결이 끊겼을 때 호출됩니다."""
        logger.info(f"Player {player_id} disconnected from game.")
        self.active = False
        await self._send_message(
            self.get_opponent_id(player_id=player_id),
            MessageType.PING,
            {"message": f"Player {player_id} has disconnected."}
        )

    async def stop(self):
        self.active = False
        
        player1 = await self.registry_manager.get_player_instance(1)
        player2 = await self.registry_manager.get_player_instance(2)
        try:
            
            if not player1.websocket.application_state == "CLOSED":
                await player1.websocket.close()
            
            if not player2.websocket.application_state == "CLOSED":
                await player2.websocket.close()
            
            
            logger.info("stop에서 닫음")
        except Exception as e:
            logger.error(f"Error while stopping game: {e}")


    async def send_available_move(self, player_id:int):
        condition_info = ConditionInfo(
            player_id=player_id,
            trigger_cards=self.trigger_cards
        )
        
        player = await self.registry_manager.get_player_instance(player_id)
        available_effects = await player.get_available_effects(condition_info)
        message = []
        for effect_id in available_effects:
            effect = await self.registry_manager.get_effect_instance(effect_id)
            message.append(Move(move_type=MoveType.EFFECT,
                            entity=await self.card_to_entity(card_id=effect.card_id, player_id=player_id),
                            select=effect.select,
                            targets=await effect.targets(condition_info),
                            effect_id=effect_id))
        await self._send_message(player_id=player_id, message_type=MessageType.MOVE, data=message)
        return available_effects
        
        
    async def card_to_entity(self, card_id:int, player_id:int):
        card = await self.registry_manager.get_card_instance(card_id)
        player = await self.registry_manager.get_player_instance(card.player_id)
        if card.zone == ZoneType.HAND:
            index = player.hands.index(card_id)
        elif card.zone == ZoneType.FIELD:
            for key in player.fields.keys():
                if player.fields[key] == card_id:
                    index = key
        elif card.zone == ZoneType.GRAVE:
            index = player.graves.index(card_id)
        else:
            index = None
        
        return Entity(
            type=card.zone,
            index=index,
            opponent = player_id != card.player_id
        )
    
    async def send_action(self, player_id:int, action_type: ActionType, action_data):
        await self._send_message(player_id=player_id,
                                message_type= MessageType.ACRION,
                                data=Action(
                                    action_type=action_type,
                                    action_data=action_data
                                ))

    