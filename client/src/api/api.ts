import axios, { AxiosResponse } from 'axios';
import { useRecoilState, useRecoilValue, useSetRecoilState } from 'recoil';
import { io, Socket } from 'socket.io-client';
import { decksState, userIdState } from '../atom';

class webSocket {
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

export default new webSocket();



// HTTP 요청
export const http = async (
  type: "get" | "put" | "post",
  url: string,
  callback: (data: any) => void,
  data: any = undefined,
  setLoading: ((loading: boolean) => void) | null = null) => {
  
  if (setLoading) setLoading(true);

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
    if (setLoading) setLoading(false);
  }
}


export const GetDecks = (userId:number, setDecks:(data:any)=>void,setLoading:((data:any) => void) | null = null) =>{
  http('get', `/decks/${userId}`,(data)  => {console.log(data);setDecks(data);},undefined,setLoading)
}

export const PostDecks = (userId:number, 
  deck_name:string = `새로운 덱`, 
  image:string = "0.png", 
  setLoading:((data:any) => void) | null = null
  ) => {
  http('post', `/decks/`,
  console.log,
  {
    player_id: userId,
    deck_name: deck_name,
    image: image},
    setLoading
  )
}

export const PostPlayer = (username: string, password:string, callback: (data:any) => void, setLoading:((data:any) => void) | null = null) =>{
  http("post",`/players/login`,
    callback, {
      username: username,
      password: password},
    setLoading
  )
}

export const PutPlyaer = (username:string, password:string, 
  callback : (data:any) => void, 
  setLoading:((data:any) => void) | null = null) => {

  http('put', `/players/create`, 
    callback,
    {
      username: username,
      password: password},
    setLoading
  )
}