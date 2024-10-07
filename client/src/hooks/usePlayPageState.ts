import { useState } from "react";
import { useRecoilState } from "recoil";
import { gameStatState } from "../atoms/play";
import { CardInfo, Entity, GameInfo, MessageModel } from "../types/games";
import {
  Action,
  ActionMove,
  ActionCardState,
  ActionSideEffect,
  ActionCost,
  ActionAttack,
  ActionDestroy,
  ActionDamage,
  ActionEffect,
} from "../types/action";
import { usePlayerState } from "./usePlayerState";

export const usePlayPageState = () => {
  const [showCardInfo, setShowCardInfo] = useState<CardInfo | null>(null);
  const [gameStat, setGamestat] = useRecoilState(gameStatState);
  const player = usePlayerState();


  const updateCardInfo = (card: CardInfo) => {
    setShowCardInfo(card);
  };

  

  const handleMessage = (message: string) => {
    let messageJson: MessageModel = JSON.parse(message);
    console.log(messageJson);
    switch (messageJson.type) {
      case "text":
        // 텍스트 메시지 처리
        break;
      case "game_info":
        let game_info: GameInfo = messageJson.data;
        handleMessageGameInfo(game_info)
        break;
      case "action":
        let action: Action = messageJson.data;
        handleMessageAction(action);
        break;
      default:
        console.log(messageJson);
    }
  };

  const handleMessageGameInfo = (game_info: GameInfo) => {
    setGamestat({
      is_player_turn: game_info.is_player_turn,
      turn: game_info.turn,
      side_effects: game_info.side_effects,
    });
    player.setPlayer({
      cost: game_info.Player.cost,
      health: game_info.Player.health,
      side_effects: game_info.Player.side_effects,
    });
    player.setHands(game_info.Player.hands);
    player.setFields(game_info.Player.fields);
    player.setGraves(game_info.Player.graves);
    player.setDecks(game_info.Player.decks);
  }

  const handleMessageAction = (action: Action) => {
    switch (action.action_type) {
      case "move": {
        const actionMove: ActionMove = action.action_data;
        const { before, after } = actionMove;

        const card = player.getEntity(before);
        if (!card) {
          console.log("이동하려는 카드를 찾을 수 없습니다.");
          return;
        }

        player.removeCardFromZone(before);
        player.addCardToZone(after, card);
        break;
      }
      case "card_state": {
        const actionCardState: ActionCardState = action.action_data;
        const { entity, state } = actionCardState;

        player.updateCardInZone(entity, state);
        break;
      }
      case "side_effect": {
        const actionSideEffect: ActionSideEffect = action.action_data;
        const { entity, effect } = actionSideEffect;

        if (entity.zone === "player") {
          player.setSideEffects((prevEffects) => [
            ...prevEffects,
            effect,
          ]);
        } else {
          const card = player.getEntity(entity);
          if (card) {
            const updatedCard = {
              ...card,
              side_effects: [...card.side_effects, effect],
            };
            player.updateCardInZone(entity, updatedCard);
          }
        }
        break;
      }
      case "cost": {
        const actionCost: ActionCost = action.action_data;
        const { cost } = actionCost;
        player.setCost(cost);
        break;
      }
      case "attack": {
        const actionAttack: ActionAttack = action.action_data;
        const { subject, object } = actionAttack;
        console.log(
          `공격: ${JSON.stringify(subject)}가 ${JSON.stringify(
            object
          )}를 공격했습니다.`
        );
        break;
      }
      case "destroy": {
        const actionDestroy: ActionDestroy = action.action_data;
        const { entity } = actionDestroy;

        const card = player.getEntity(entity);
        if (!card) {
          console.log("파괴할 카드를 찾을 수 없습니다.");
          return;
        }

        console.log(`카드 파괴: ${entity}`);
        break;
      }
      case "damage": {
        const actionDamage: ActionDamage = action.action_data;
        const { entity, damage } = actionDamage;

        if (entity.zone === "player") {
          player.setHealth((prevHealth) => prevHealth - damage);
        } else {
          const card = player.getEntity(entity);
          if (card && card.health !== null) {
            const updatedCard = {
              ...card,
              health: card.health - damage,
            };
            player.updateCardInZone(entity, updatedCard);
          }
        }
        break;
      }
      case "effect": {
        const actionEffect: ActionEffect = action.action_data;
        const { effect, subject, targets } = actionEffect;
        console.log(
          `효과 ${effect}가 ${JSON.stringify(subject)}에서 ${JSON.stringify(
            targets
          )}에게 적용되었습니다.`
        );
        break;
      }
      default:
        console.log("알 수 없는 액션 타입:", action);
    }
  };

  

  return {
    handleMessage,
    showCardInfo,
    gameStat,
    setGamestat,
    updateCardInfo,
  };
};
