import { http } from './api';

type setFn = (data: any) => void;

export const GetPlayer = (userId: number, setPlayer: setFn, setLoading: setFn) => {
  http('get', `/players/state/${userId}`, setPlayer, setLoading);
}

export const GetPlayerCards = (userId: number, setPlayerCards: setFn, setLoading: setFn) => {
  http('get', `/players/cards/${userId}`, setPlayerCards, setLoading);
}

export const PostPlayer = (username: string, password: string, callback: setFn, setLoading: setFn) => {
  http("post", `/players/login`, callback, setLoading, {
    username: username,
    password: password
  });
}

export const PutPlayer = (username: string, password: string, callback: setFn, setLoading: setFn) => {
  http('put', `/players/create/${username}/${password}`, callback, setLoading);
}
