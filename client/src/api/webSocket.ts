import { io, Socket } from 'socket.io-client';

class WebSocketService {
  private socket: Socket | null = null;

  connectWebSocket(url: string, messageHandler: (message: any) => void): void {
    this.socket = io(url);

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
    });

    this.socket.on('message', (message: any) => {
      console.log('WebSocket message received:', message);
      messageHandler(message);
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  }

  sendWebSocketMessage(message: string): void {
    if (this.socket) {
      this.socket.emit('message', message);
    } else {
      console.error('WebSocket is not connected');
    }
  }

  closeWebSocket(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    } else {
      console.error('WebSocket is not connected');
    }
  }
}

export const webSocketService = new WebSocketService();
