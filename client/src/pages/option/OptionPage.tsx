// src/pages/option/OptionPage.tsx

import React, { useState, useEffect } from "react";
import WebSocketClient from "../../api/websocket"; // WebSocketClient 싱글톤 클래스 import
import { useSetRecoilState } from "recoil";
import { showPageState } from "../../atoms/global";

const OptionPage: React.FC = () => {
  const setShowPage = useSetRecoilState(showPageState);
  const [isConnected, setIsConnected] = useState(false);
  const [message, setMessage] = useState("");
  const [receivedMessages, setReceivedMessages] = useState<string[]>([]);

  const client = WebSocketClient.getInstance("ws://localhost:8000/ws");

  useEffect(() => {
    if (isConnected) {
      client.connect((receivedMessage) => {
        // 메시지 수신 시 처리할 로직
        setReceivedMessages((prevMessages) => [
          ...prevMessages,
          receivedMessage,
        ]);
      });
    }

    // 컴포넌트가 언마운트되거나 연결 상태가 변경될 때 WebSocket을 닫습니다.
    return () => {
      client.close();
      setIsConnected(false);
    };
  }, [isConnected]);

  const handleConnect = () => {
    setIsConnected(true);
  };

  const handleDisconnect = () => {
    client.close();
    setIsConnected(false);
  };

  const handleSendMessage = () => {
    if (message.trim()) {
      client.sendMessage(message);
      setMessage("");
    }
  };

  return (
    <div>
      <button onClick={() => {setShowPage("home")}}>exit</button>
      <h1>WebSocket 연결</h1>
      <button onClick={handleConnect} disabled={isConnected}>
        {isConnected ? "Connected" : "Connect"}
      </button>
      <button onClick={handleDisconnect} disabled={!isConnected}>
        Disconnect
      </button>

      {isConnected && (
        <div>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Send a message"
          />
          <button onClick={handleSendMessage} disabled={!message.trim()}>
            Send
          </button>
        </div>
      )}

      <ul>
        {receivedMessages.map((msg, index) => (
          <li key={index}>{msg}</li>
        ))}
      </ul>
    </div>
  );
};

export default OptionPage;
