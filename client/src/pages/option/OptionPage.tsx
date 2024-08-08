import React, { useState, useEffect } from 'react';
import WebSocketClient from '../../api/websocket'; // WebSocketClient 싱글톤 클래스 import

const OptionPage: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [message, setMessage] = useState('');
  const [receivedMessages, setReceivedMessages] = useState<string[]>([]);


  const client = WebSocketClient.getInstance('ws://localhost:3000/ws');

  const connectWebSocket = () => {
    client.connect((receivedMessage) => {
      // 메시지 수신 시 처리할 로직
      setReceivedMessages((prevMessages) => [...prevMessages, receivedMessage]);
    });

    setIsConnected(true);
  };

  const sendMessage = () => {
    client.sendMessage(message);
    setMessage('');
  };

  // 연결 상태를 추적하여 컴포넌트가 언마운트될 때 WebSocket을 닫습니다.
  useEffect(() => {
    return () => {
      client.close();
    };
  }, [client]);

  return (
    <div>
      <h1>WebSocket 연결</h1>
      <button onClick={connectWebSocket} disabled={isConnected}>
        {isConnected ? 'Connected' : 'Connect'}
      </button>

      {isConnected && (
        <div>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Send a message"
          />
          <button onClick={sendMessage}>Send</button>
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
