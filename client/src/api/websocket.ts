class WebSocketClient {
  private url: string;
  private websocket: WebSocket | null;

  constructor(url: string) {
    this.url = url;
    this.websocket = null;
  }

  connect(
    token: string,
    onMessage: (message: string) => void,
    onClose: (event: CloseEvent) => void
  ) {
    this.websocket = new WebSocket(`${this.url}?token=${token}`);

    this.websocket.onopen = () => {
      console.log('WebSocket connection opened');
    };

    this.websocket.onmessage = (event: MessageEvent) => {
      const message = event.data;
      console.log('Message received from server:', message);
      onMessage(message);
    };

    this.websocket.onclose = (event: CloseEvent) => {
      console.log('WebSocket connection closed', event);
      onClose(event);
    };

    this.websocket.onerror = (error: Event) => {
      console.error('WebSocket error:', error);
    };
  }

  sendMessage(message: string) {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      console.log('Sending message to server:', message);
      this.websocket.send(message);
    } else {
      console.error('WebSocket is not open. Cannot send message.');
    }
  }

  disconnect() {
    if (this.websocket) {
      this.websocket.close(4000, 'Client initiated disconnect');
    }
  }
}

export default WebSocketClient;
