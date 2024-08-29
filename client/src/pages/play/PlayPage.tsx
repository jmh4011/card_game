import React, { useEffect, useRef, useState } from "react";
import { useRecoilState, useRecoilValue } from "recoil";
import { wsTokenState } from "../../atoms/global";
import WebSocketClient from "../../api/websocket";
import PlayHomePage from "./PlayHomePage";

const PlayPage: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([]);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const wsClientRef = useRef<WebSocketClient | null>(null);
  const token = useRecoilValue(wsTokenState);

  useEffect(() => {
    wsClientRef.current = new WebSocketClient();

    // 컴포넌트 언마운트 시 WebSocket 연결 종료
    return () => {
      if (wsClientRef.current) {
        wsClientRef.current.disconnect();
      }
    };
  }, []);

  const toggleConnection = () => {
    if (!wsClientRef.current) return;

    if (isConnected) {
      wsClientRef.current.disconnect();
      setIsConnected(false);
    } else {
      wsClientRef.current.connect(
        token,
        (message) => {
          setMessages((prevMessages) => [...prevMessages, message]);
        },
        () => {
          console.log("Connection closed by server");
          setIsConnected(false);
        }
      );
      setIsConnected(true);
    }
  };

  const handleSendMessage = () => {
    if (wsClientRef.current) {
      wsClientRef.current.sendMessage("Hello, Server!");
    }
  };

  return <div></div>;
};

export default PlayPage;
