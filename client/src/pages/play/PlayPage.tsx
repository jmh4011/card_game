// PlayPage.tsx

import React, { useEffect, useRef, useState } from 'react';
import { useRecoilState } from 'recoil';
import WebSocketClient from '../../api/websocket';
import useHttpGame from '../../api/game';
import styled from 'styled-components';
import PlayerField from '../../components/plays/PlayerField';
import ShowCardInfo from '../../components/plays/ShowCardInfo';
import { CardInfo, Entity, GameInfo, MessageModel } from '../../types/games';
import { gameStatState } from '../../atoms/play';
import {
  Action,
  ActionAttack,
  ActionCardState,
  ActionCost,
  ActionDamage,
  ActionDestroy,
  ActionEffect,
  ActionMove,
  ActionSideEffect,
} from '../../types/action';
import { usePlayerStateActions } from '../../utils/playerStateUtils';

const PlayPage: React.FC = () => {
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const wsClientRef = useRef<WebSocketClient | null>(null);
  const { getToken } = useHttpGame();
  const [showCardInfo, setShowCardInfo] = useState<CardInfo | null>(null);
  const [gameStat, setGamestat] = useRecoilState(gameStatState);

  // 상태 업데이트 액션들
  const playerActions = usePlayerStateActions();

  // getEntity 함수 수정
  const getEntity = (entity: Entity): CardInfo | null => {
    switch (entity.zone) {
      case 'hands':
      case 'fields':
      case 'graves':
        return playerActions[entity.zone][entity.index] || null;
      case 'decks':
        return null; // decks의 구현 방식에 따라 수정 필요
      case 'player':
        return null; // 플레이어 자체를 반환하는 경우 처리 필요
      default:
        return null;
    }
  };

  const handleCard = (val: CardInfo) => {
    setShowCardInfo(val);
  };

  const handleMessage = (message: string) => {
    let messageJson: MessageModel = JSON.parse(message);
    console.log(messageJson);
    switch (messageJson.type) {
      case 'text':
        // 텍스트 메시지 처리
        break;
      case 'game_info':
        let gameInfo: GameInfo = messageJson.data;
        setGamestat({
          is_player_turn: gameInfo.is_player_turn,
          turn: gameInfo.turn,
          side_effects: gameInfo.side_effects,
        });
        playerActions.setPlayer({
          cost: gameInfo.Player.cost,
          health: gameInfo.Player.health,
          side_effects: gameInfo.Player.side_effects,
        });
        playerActions.setHands(gameInfo.Player.hands);
        playerActions.setFields(gameInfo.Player.fields);
        playerActions.setGraves(gameInfo.Player.graves);
        playerActions.setDecks(gameInfo.Player.decks);
        break;
      case 'action':
        let action: Action = messageJson.data;
        handleMessageAction(action);
        break;
      default:
        console.log(messageJson);
    }
  };

  const handleMessageAction = (action: Action) => {
    switch (action.action_type) {
      case 'move': {
        const actionMove: ActionMove = action.action_data;
        const { before, after } = actionMove;

        const card = getEntity(before);
        if (!card) {
          console.log('이동하려는 카드를 찾을 수 없습니다.');
          return;
        }

        // 카드 제거 및 추가
        playerActions.removeCardFromZone(before);
        playerActions.addCardToZone(after, card);

        break;
      }
      case 'card_state': {
        const actionCardState: ActionCardState = action.action_data;
        const { entity, state } = actionCardState;

        // 카드 상태 업데이트
        playerActions.updateCardInZone(entity, state);

        break;
      }
      case 'side_effect': {
        const actionSideEffect: ActionSideEffect = action.action_data;
        const { entity, effect } = actionSideEffect;

        if (entity.zone === 'player') {
          playerActions.setSideEffects((prevEffects) => [...prevEffects, effect]);
        } else {
          const card = getEntity(entity);
          if (card) {
            const updatedCard = {
              ...card,
              side_effects: [...card.side_effects, effect],
            };
            playerActions.updateCardInZone(entity, updatedCard);
          }
        }
        break;
      }
      case 'cost': {
        const actionCost: ActionCost = action.action_data;
        const { cost } = actionCost;
        playerActions.setCost(cost);
        break;
      }
      case 'attack': {
        const actionAttack: ActionAttack = action.action_data;
        const { subject, object } = actionAttack;
        console.log(
          `공격: ${JSON.stringify(subject)}가 ${JSON.stringify(
            object
          )}를 공격했습니다.`
        );
        break;
      }
      case 'destroy': {
        const actionDestroy: ActionDestroy = action.action_data;
        const { entity} = actionDestroy;
        
        const card = getEntity(entity);
        if (!card) {
          console.log('파괴할 카드를 찾을 수 없습니다.');
          return;
        }

        // 파괴 로그 출력
        console.log(
          `카드 파괴: ${entity}`
        );

        break;
      }
      case 'damage': {
        const actionDamage: ActionDamage = action.action_data;
        const { entity, damage } = actionDamage;

        if (entity.zone === 'player') {
          playerActions.setHealth((prevHealth) => prevHealth - damage);
        } else {
          const card = getEntity(entity);
          if (card && card.health !== null) {
            const updatedCard = {
              ...card,
              health: card.health - damage,
            };
            playerActions.updateCardInZone(entity, updatedCard);
          }
        }
        break;
      }
      case 'effect': {
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
        console.log('알 수 없는 액션 타입:', action);
    }
  };

  const handleDrop = (index: number, cardIndex: number) => {
    wsClientRef.current?.sendMessage(
      `Card with index ${cardIndex} dropped on field ${index}`
    );
  };

  useEffect(() => {
    getToken((data) => {
      wsClientRef.current = new WebSocketClient();
      wsClientRef.current.connect(data, handleMessage, () => {
        console.log('Connection closed by server');
        setIsConnected(false);
      });
      setIsConnected(true);
    });

    return () => {
      if (wsClientRef.current) {
        wsClientRef.current.disconnect();
        setIsConnected(false);
      }
    };
  }, []);

  return (
    <Container>
      <Enemy>{/* 상대 플레이어 필드 */}</Enemy>
      {showCardInfo && (
        <CardInfoContainer>
          <ShowCardInfo card={showCardInfo} />
        </CardInfoContainer>
      )}
      <My>
        <PlayerField handleCard={handleCard} handleDrop={handleDrop} />
      </My>
    </Container>
  );
};

export default PlayPage;

const Container = styled.div`
  width: 100%;
  height: 100%;
  flex-direction: column;
  display: flex;
  overflow: hidden;
`;

const Enemy = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 50%;
  border: 3px solid rgb(100, 0, 0);
  transform: scale(1, -1);
`;

const My = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 50%;
  border: 3px solid rgb(0, 0, 100);
`;

const CardInfoContainer = styled.div`
  position: fixed;
  top: 50%;
  transform: translate(0, -50%);
  z-index: 1;
  width: 30vh;
  height: 40vh;
  border: 1px solid rgb(100, 0, 100);
`;
