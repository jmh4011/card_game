import React, { useEffect, useRef, useState } from "react";
import { useRecoilState, useRecoilValue } from "recoil";
import { cardsStats, wsTokenState } from "../../atoms/global";
import WebSocketClient from "../../api/websocket";
import useHttpGame from "../../api/game";
import styled from "styled-components";
import PlayerField from "../../components/plays/PlayerField";
import ShowCardInfo from "../../components/plays/ShowCardInfo";
import { Card } from "../../types/models";
import { Action, CardInfo, GameInfo, MessageModel } from "../../types/games";
import {
  gameStatState,
  playerDecksState,
  playerFieldsState,
  playerGravesState,
  playerHandsState,
  playerStatState,
} from "../../atoms/play";

const PlayPage: React.FC = () => {
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const wsClientRef = useRef<WebSocketClient | null>(null);
  const { getToken } = useHttpGame();
  const [gameStat, setGamestat] = useRecoilState(gameStatState);
  const [playerStat, setPlayerStat] = useRecoilState(playerStatState);
  const [playerHands, setPlayerHands] = useRecoilState(playerHandsState);
  const [playerFields, setPlayerFields] = useRecoilState(playerFieldsState);
  const [playerGraves, setPlayerGraves] = useRecoilState(playerGravesState);
  const [playerDecks, setPlayerDecks] = useRecoilState(playerDecksState);
  const [showCardInfo, setShowCardInfo] = useState<CardInfo | null>(null);

  const handleCard = (val: CardInfo) => {
    setShowCardInfo(val);
  };

  const handleMessage = (message: string) => {
    let messageJson: MessageModel = JSON.parse(message);
    console.log(messageJson);
    switch (messageJson.type) {
      case "text":
        let data: string = messageJson.data;
        break;
      case "gameinfo":
        let gameInfo: GameInfo = messageJson.data;
        setGamestat({
          is_player_turn: gameInfo.is_player_turn,
          trun: gameInfo.trun,
          side_effects: gameInfo.side_effects,
        });
        setPlayerStat({
          health: gameInfo.Player.health,
          cost: gameInfo.Player.cost,
          side_effects: gameInfo.Player.side_effects,
        });
        setPlayerHands(gameInfo.Player.hands);
        setPlayerFields(gameInfo.Player.fields);
        setPlayerGraves(gameInfo.Player.graves);
        setPlayerDecks(gameInfo.Player.decks);
        break;
      case "action":
        let action: Action = messageJson.data;
        break;
      default:
        console.log(messageJson);
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
        console.log("Connection closed by server");
        setIsConnected(false);
      });
      setIsConnected(true);
    });

    // 컴포넌트 언마운트 시 WebSocket 연결 종료
    return () => {
      if (wsClientRef.current) {
        wsClientRef.current.disconnect();
        setIsConnected(false);
      }
    };
  }, []);

  return (
    <Contener>
      <Enemy>{/* <PlayerField handleCard={handleCard}/> */}</Enemy>
      {showCardInfo ? (
        <CardInfoContener>
          <ShowCardInfo card={showCardInfo} />
        </CardInfoContener>
      ) : null}
      <My>
        <PlayerField handleCard={handleCard} handleDrop={handleDrop} />
      </My>
    </Contener>
  );
};

export default PlayPage;

const Contener = styled.div`
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
const Center = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 30%;
  border: 3px solid rgb(0, 0, 0);
`;

const My = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 50%;
  border: 3px solid rgb(0, 0, 100);
`;

const CardInfoContener = styled.div`
  position: fixed;
  top: 50%;
  transform: translate(0, -50%);
  z-index: 1;
  width: 30vh;
  height: 40vh;
  border: 1px solid rgb(100, 0, 100);
`;
