// src/api/api.ts
import axios, { AxiosResponse } from 'axios';
import { SetterOrUpdater } from 'recoil';
import { io, Socket } from 'socket.io-client';

type setFn = (data:any) => void;

class WebSocketService {
  private socket: Socket | null = null;
  // WebSocket 연결
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

  // WebSocket 메시지 전송
  sendWebSocketMessage(message: string): void {
    if (this.socket) {
      this.socket.emit('message', message);
    } else {
      console.error('WebSocket is not connected');
    }
  }

  // WebSocket 연결 닫기
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

// HTTP 요청
export const http = async (
  type: "get" | "put" | "post",
  url: string,
  callback: (data: any) => void,
  setLoading: setFn,
  data: any = undefined) => {
  
  setLoading(true);
  
  const request = type === 'get' ? axios.get : type === "put"? axios.put: axios.post;

  try {
    const response: AxiosResponse = data === undefined 
      ? await request(url) 
      : await request(url, data);
    callback(response.data);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Error response:', error.response);
      console.error('Detail:', error.response?.data?.detail);
    } else {
      console.error('Unexpected error:', error);
    }
  } finally {
    setLoading(false);
  }
}


export const GetDecks = (userId:number, setDecks:setFn, setLoading: setFn) => {
  http('get', `/decks/${userId}`,setDecks, setLoading);
}

export const PostDecks = (userId:number, setDeck:setFn, setLoading: setFn,
  deck_name:string = `새로운 덱`, 
  image:string = "0.png") => {
  http('post', `/decks/`, setDeck, setLoading, {
    player_id: userId,
    deck_name: deck_name,
    image: image
  });
}

export const GetPlayer = (userId:number, setPlayer:setFn, setLoading: setFn) => {
  http('get', `/players/state/${userId}`, setPlayer, setLoading);
}

export const GetPlayerCards = (userId:number, setPlayerCards: setFn, setLoading: setFn) =>{
  http('get', `/players/cards/${userId}`, setPlayerCards,setLoading)
}

export const PostPlayer = (username: string, password:string, callback: setFn, setLoading: setFn) => {
  http("post", `/players/login`, callback, setLoading, {
    username: username,
    password: password
  });
}

export const PutPlayer = (username:string, password:string, 
  callback: setFn, setLoading: setFn) => {
  http('put', `/players/create/${username}/${password}`, callback, setLoading);
}

export const GetDeckPlayerCards = (deck_id: number, userId:number,callback: setFn, setLoading: setFn) => {
  http('get', `/decks/cards/${deck_id}/${userId}`, callback, setLoading);
}

interface deckUpdate {
  deck_name: string;
  image: string;
  deck_cards: number[]
}

export const PutDeckUpdate = (deck_id: number,data:deckUpdate,setDeck: setFn,setDeckCrads:setFn,setLoading: setFn) => {
  http('put', `/decks/${deck_id}`, (data:any) => {
    setDeck(data.deck);
    setDeckCrads(data.deck_cards)},
    setLoading, data)
}