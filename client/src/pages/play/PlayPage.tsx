import React, { useEffect, useRef, useState } from "react";
import { useRecoilState, useRecoilValue } from "recoil";
import { cardsStats, wsTokenState } from "../../atoms/global";
import WebSocketClient from "../../api/websocket";
import PlayHomePage from "./PlayHomePage";
import useHttpGame from "../../api/game";
import styled from "styled-components";
import PlayerField from "./components/PlayerField";
import CardInfo from "./components/CardInfo";
import { Card } from "../../utils/types";

const PlayPage: React.FC = () => {
  const cards = useRecoilValue(cardsStats);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const wsClientRef = useRef<WebSocketClient | null>(null);
  const { getToken } = useHttpGame();

  const [hands, setHands] = useState<number[]>([1, 2, 3, 3]);
  const [fields, setFields] = useState<Record<number, Card>>({});
  const [graves, setGraves] = useState<Card[]>([]);
  const [decks, setDecks] = useState<number>(40);
  const [showCardInfo, setShowCardInfo] = useState<number>(1)

  const handleCard = (val:number) => {
    setShowCardInfo(val)
  }

  const handleSubmit = (data:string) => {
    try {
      console.log((JSON.parse(data)));
    } catch (error) {
      console.log(data);
    }
  };

  const handleDrop = (index: number, cardIndex: number) => {
    wsClientRef.current?.sendMessage(`Card with index ${cardIndex} dropped on field ${index}`);
  };
  

  useEffect(() => {
    getToken((data) => {
      wsClientRef.current = new WebSocketClient();
      wsClientRef.current.connect(
        data,
        (message) => {
          handleSubmit(message)
        },
        () => {
          console.log("Connection closed by server");
          setIsConnected(false);
        }
      );
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
      <Enemy>
        {/* <PlayerField handleCard={handleCard}/> */}
      </Enemy>
      <CardInfoContener>
        <CardInfo card_id={showCardInfo} />
      </CardInfoContener>
      <My>
        <PlayerField handleCard={handleCard} handleDrop={handleDrop}/>
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
  transform: scale(1, -1)
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
