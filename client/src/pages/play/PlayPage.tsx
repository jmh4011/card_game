import React, { useEffect, useRef, useState } from "react";
import { useRecoilState, useRecoilValue } from "recoil";
import { wsTokenState } from "../../atoms/global";
import WebSocketClient from "../../api/websocket";
import PlayHomePage from "./PlayHomePage";
import useHttpGame from "../../api/game";

const PlayPage: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([]);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const wsClientRef = useRef<WebSocketClient | null>(null);
  const { getToken } = useHttpGame();

  useEffect(() => {
    getToken((data) => {
      wsClientRef.current = new WebSocketClient();
      wsClientRef.current.connect(
        data,
        (message) => {
          setMessages((prevMessages) => [...prevMessages, message]);
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

  const handleSendMessage = () => {
    if (wsClientRef.current) {
      wsClientRef.current.sendMessage("Hello, Server!");
    }
  };

  return (
    <div>
      <button onClick={handleSendMessage}>메ㅔㅔㅔㅔㅔㅔㅔㅔ</button>
    </div>
  );
};

export default PlayPage;
