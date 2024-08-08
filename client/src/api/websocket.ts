type MessageHandler = (message: string) => void;

class WebSocketClient {
  private static instance: WebSocketClient | null = null;
  private socket: WebSocket | null = null;
  private messageHandler: MessageHandler | null = null;
  private url: string;
  private shouldReconnect: boolean;
  private reconnectInterval: number; // 재연결 시도 간격 (밀리초)
  private maxRetries: number; // 최대 재연결 시도 횟수
  private retryCount: number;
  private intentionalCloseCode: number; // 의도적인 종료 코드

  // private constructor to prevent direct instantiation
  private constructor(
    url: string,
    reconnectInterval = 1000,
    maxRetries = 10,
    intentionalCloseCode = 4000 // 서버에서 의도적으로 종료 시 사용하는 코드
  ) {
    this.url = url;
    this.shouldReconnect = true;
    this.reconnectInterval = reconnectInterval;
    this.maxRetries = maxRetries;
    this.retryCount = 0;
    this.intentionalCloseCode = intentionalCloseCode;
  }

  public static getInstance(
    url: string,
    reconnectInterval = 1000,
    maxRetries = 10,
    intentionalCloseCode = 4000
  ): WebSocketClient {
    if (!WebSocketClient.instance) {
      WebSocketClient.instance = new WebSocketClient(
        url,
        reconnectInterval,
        maxRetries,
        intentionalCloseCode
      );
    }
    return WebSocketClient.instance;
  }

  public connect(onMessage: MessageHandler) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log("WebSocket already connected.");
      return;
    }

    this.messageHandler = onMessage;
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      console.log("WebSocket connection established.");
      this.retryCount = 0; // 재연결 성공 시 시도 횟수 초기화
    };

    this.socket.onmessage = (event: MessageEvent) => {
      console.log("Message received:", event.data);
      if (this.messageHandler) {
        this.messageHandler(event.data);
      }
    };

    this.socket.onclose = (event: CloseEvent) => {
      console.log(`WebSocket connection closed with code: ${event.code}.`);

      switch (event.code) {
        case this.intentionalCloseCode:
          console.log("WebSocket connection intentionally closed by server.");
          this.shouldReconnect = false;
          break;
        case 1008:
          console.log("Connection rejected by server: Policy Violation.");
          this.shouldReconnect = false;
          break;
        default:
          if (this.shouldReconnect) {
            this.retryConnection();
          }
          break;
      }
    };


    this.socket.onerror = (error) => {
      console.error("WebSocket error:", error);
      this.socket?.close();
    };
  }

  private retryConnection() {
    if (this.retryCount < this.maxRetries) {
      console.log(
        `Attempting to reconnect... (${this.retryCount + 1}/${this.maxRetries})`
      );
      setTimeout(() => {
        this.retryCount++;
        if (this.messageHandler) {
          this.connect(this.messageHandler);
        }
      }, this.reconnectInterval);
    } else {
      console.error("Max reconnect attempts reached. Could not reconnect.");
    }
  }

  public sendMessage(message: string) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message);
      console.log("Message sent:", message);
    } else {
      console.error("WebSocket is not open. Cannot send message:", message);
    }
  }

  public close() {
    this.shouldReconnect = false; // 수동 종료 시에는 재연결하지 않음
    if (this.socket) {
      this.socket.close();
    }
  }
}

export default WebSocketClient;
