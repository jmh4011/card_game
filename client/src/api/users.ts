import { useHttp } from './api';
import { SetFn } from '../utils/types';

const useHttpUser = () => {
  const { http } = useHttp();

  const userLogin = (username: string, password: string, callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "put",
      url: `/users/login`,
      callback:callback,
      onError:onError,
      customSetLoading: setLoading,
      data: { username, password }
    });
  }

  const userLogout = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "delete",
      url: `/users/logout`,
      callback:callback,
      onError:onError,
      customSetLoading: setLoading
    });
  }

  const createUser = (username: string, password: string, callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "post",
      url: `/users/create`,
      callback:callback,
      onError:onError,
      customSetLoading: setLoading,
      data: { username, password }
    });
  }

  const getUserState = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/users/state`,
      callback:callback,
      onError:onError,
      customSetLoading: setLoading
    });
  }

  const getUserCards = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/users/cards`,
      callback:callback,
      onError:onError,
      customSetLoading: setLoading
    });
  }

  const setUserDeckSelection = (mode : string,callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "post",
      url: `/users/cards`,
      callback:callback,
      onError:onError,
      customSetLoading: setLoading
    });
  }
  return { userLogin, userLogout, createUser, getUserState, getUserCards};
}


export default useHttpUser