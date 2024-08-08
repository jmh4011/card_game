import { useHttp } from './api';
import { DeckSelectionUpdate, SetFn } from '../utils/types';

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

  const getUserStat = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/users/stat`,
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

  const getUserDeckSelection = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/users/deck-selection`,
      callback:callback,
      onError:onError,
      customSetLoading: setLoading,
    });
  }

  const updateUserDeckSelection = (data: DeckSelectionUpdate,callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "put",
      url: `/users/deck-selection`,
      callback:callback,
      onError:onError,
      customSetLoading: setLoading,
      data:data
    });
  }
  return { userLogin, userLogout, createUser, getUserStat, getUserCards, updateUserDeckSelection, getUserDeckSelection};
}


export default useHttpUser