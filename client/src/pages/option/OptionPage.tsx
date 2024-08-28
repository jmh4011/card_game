// src/pages/option/OptionPage.tsx

import React, { useState, useEffect, useRef } from "react";
import WebSocketClient from "../../api/websocket"; // WebSocketClient 싱글톤 클래스 import
import { useRecoilState, useRecoilValue, useSetRecoilState } from "recoil";
import useHttpGame from "../../api/game";
import { wsTokenState } from "../../atoms/global";
import { useNavigate } from "react-router-dom";

const OptionPage: React.FC = () => {
  const navigate = useNavigate();
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

  return (
    <div>
      <button
        onClick={() => {
          navigate("/");
        }}
      >
        exit
      </button>
      <h1>WebSocket Messages</h1>
      <button onClick={toggleConnection}>
        {isConnected ? "Disconnect" : "Connect"}
      </button>
      <button onClick={handleSendMessage} disabled={!isConnected}>
        Send Message
      </button>
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>{msg}</li>
        ))}
      </ul>
    </div>
  );
};

export default OptionPage;
