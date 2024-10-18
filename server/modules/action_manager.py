
from modules.game_manager import GameManager
from server.schemas.game.action import ActionCreateCard, ActionMove, ActionType
from server.schemas.game.entity import Entity, EntityType
from server.schemas.game.enums import ZoneType


class ActionManager:
    def __init__(self, game_manager: 'GameManager'):
        self.game_manager = game_manager
    
    
    async def draw(self, player_id:int,num: int = 1) -> list[int]:
        """Draws cards from the deck to the hand."""
        drawn_cards = []
        player = await self.game_manager.registry_manager.get_player_instance(player_id)
        for _ in range(num):
            if not player.decks:
                break
            card_id = player.decks.pop()
            card = await self.game_manager.registry_manager.get_card_instance(card_id)
            player.hands.append(card_id)
            drawn_cards.append(card_id)
            await self.game_manager.send_action(
                player_id=player_id,
                action_type=ActionType.MOVE,
                action_data=ActionMove(
                    before=Entity(
                        index = None,
                        opponent=False,
                        type=EntityType.DECK
                    ),
                    entity=Entity(
                        index= None,
                        opponent= False,
                        type=EntityType.HAND
                    ),
                    state=card.get_info_player(),
                    destroy=False
                )
            )
            await self.game_manager.send_action(
                player_id=self.game_manager.registry_manager.get_opponent_id(player_id),
                action_type=ActionType.MOVE,
                action_data=ActionMove(
                    before=Entity(
                        index = None,
                        opponent=True,
                        type=EntityType.DECK
                    ),
                    entity=Entity(
                        index= None,
                        opponent= True,
                        type=EntityType.HAND
                    ),
                    state=card.get_info_opponet(),
                    destroy=False
                )
            )
            
        return drawn_cards
    
    
    async def move_card(self, card_id:int, player_id:int, zone:ZoneType, index: int | None = None):
        card = await self.game_manager.registry_manager.get_card_instance(card_id)
        
        before_player1_public = await card.is_public(1)
        before_player2_public = await card.is_public(2)
        before_player_id = card.player_id
        before_player = await self.game_manager.registry_manager.get_player_instance(before_player_id)
        before_zone = card.zone
        before_index = await before_player.remove_card(card_id=card_id, zone=before_zone)

        
        
        after_player = await self.game_manager.registry_manager.get_player_instance(player_id)
        await after_player.add_card_to_zone(card_id=card_id,zone=zone,index=index)
        await card.move(zone)
        
        
        if not before_player1_public and await card.is_public(1):
            await self.game_manager.send_action(
                player_id= 1,
                action_type=ActionType.MOVE,
                action_data=ActionMove(
                    before=Entity(
                        index = before_index,
                        opponent=before_player_id != 1,
                        type= before_zone
                    ),
                    after=Entity(
                        index = index,
                        opponent= False,
                        type= zone
                    ),
                    state=card._get_info(),
                    destroy=False
                )
            )
        else:
            pass
        
        if not before_opponet_public and await card.is_public_opponet():
            pass
        else:
            pass
        
        
        return card
    
