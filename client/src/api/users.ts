import { useHttp } from "./api";
import { DeckSelectionUpdate, SetFn } from "../utils/types";
import { useSetRecoilState } from "recoil";
import {
  decksState,
  userStats,
  userCardsStats,
  cardsStats,
  deckSelectionState,
  isAuthenticatedState,
} from "../atoms/global";

const useHttpUser = () => {
  const {http} = useHttp()
  const setDecks = useSetRecoilState(decksState);
  const setUser = useSetRecoilState(userStats);
  const setIsAuthenticated = useSetRecoilState(isAuthenticatedState);
  const setUserCards = useSetRecoilState(userCardsStats);
  const setCards = useSetRecoilState(cardsStats);
  const setDeckSelection = useSetRecoilState(deckSelectionState);

  const authCheck = () => {
    http({
      type: "get",
      url: `/users/auth`,
      callback: (data) => setIsAuthenticated(data),
    });
  };

  const userLogin = (
    username: string,
    password: string,
    callback: SetFn,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "put",
      url: `/users/login`,
      callback: callback,
      onError: onError,
      customSetLoading: setLoading,
      data: { username, password },
    });
  };

  const userLogout = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "delete",
      url: `/users/logout`,
      callback: callback,
      onError: onError,
      customSetLoading: setLoading,
    });
  };

  const createUser = (
    username: string,
    password: string,
    callback: SetFn,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "post",
      url: `/users/create`,
      callback: callback,
      onError: onError,
      customSetLoading: setLoading,
      data: { username, password },
    });
  };

  const getUserStat = (onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/users/stat`,
      callback: (data) => {
        setUser(data);
      },
      onError: onError,
      customSetLoading: setLoading,
    });
  };

  const getUserCards = (onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/users/cards`,
      callback: (data) => {
        setUserCards(data);
      },
      onError: onError,
      customSetLoading: setLoading,
    });
  };

  const getUserDeckSelection = (onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/users/deck-selection`,
      callback: (data) => {
        setDeckSelection(data);
      },
      onError: onError,
      customSetLoading: setLoading,
    });
  };

  const updateUserDeckSelection = (
    data: DeckSelectionUpdate,
    callback: SetFn,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "put",
      url: `/users/deck-selection`,
      callback: callback,
      onError: onError,
      customSetLoading: setLoading,
      data: data,
    });
  };
  return {
    authCheck,
    userLogin,
    userLogout,
    createUser,
    getUserStat,
    getUserCards,
    updateUserDeckSelection,
    getUserDeckSelection,
  };
};

export default useHttpUser;
