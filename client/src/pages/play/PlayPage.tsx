import React, { useEffect, useRef, useState } from "react";
import styled from "styled-components";
import { usePlayPage } from "../../hooks/usePlayPage";
import useHttpGame from "../../api/game";
import WebSocketClient from "../../api/websocket";
import PlayerField from "../../components/plays/PlayerField";

const PlayPage: React.FC = () => {
  const {handleMessage} = usePlayPage()
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const wsClientRef = useRef<WebSocketClient | null>(null);
  const { getToken } = useHttpGame();

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
      <CardInfoContener>
      </CardInfoContener>
      <My>
        <PlayerField handleDrop={handleDrop} handleCard={(val) => {console.log(val)}}/>
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
