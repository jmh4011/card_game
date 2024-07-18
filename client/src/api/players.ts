import { useHttp } from './api';
import { SetFn } from '../utils/types';

const useHttpPlayer = () => {
  const { http } = useHttp();

  const playerLogin = (username: string, password: string, callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "put",
      url: `/players/login`,
      callback,
      customSetLoading: setLoading,
      onError,
      data: { username, password }
    });
  }

  const playerLogout = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "delete",
      url: `/players/logout`,
      callback,
      onError,
      customSetLoading: setLoading
    });
  }

  const createPlayer = (username: string, password: string, callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "post",
      url: `/players/create`,
      callback,
      customSetLoading: setLoading,
      onError,
      data: { username, password }
    });
  }

  const getPlayerState = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/players/state`,
      callback,
      onError,
      customSetLoading: setLoading
    });
  }

  const getPlayerCards = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/players/cards`,
      callback,
      onError,
      customSetLoading: setLoading
    });
  }
  
  return { playerLogin, playerLogout, createPlayer, getPlayerState, getPlayerCards};
}


export default useHttpPlayer