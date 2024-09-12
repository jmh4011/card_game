import { useHttp } from "./api";
import {SetFn} from "../types/types";
import { useSetRecoilState } from "recoil";
import {
  userStats,
  userCardsStats,
  cardsStats,
  deckSelectionState,
  isAuthenticatedState,
} from "../atoms/global";
import { UserStatUpdate, DeckSelectionUpdate, UserLogin, UserSignUp, UserStat, UserCards, DeckSelection } from "../types/routers";
import { Deck } from "../types/models";

const useHttpUser = () => {
  const { http } = useHttp();
  const setUser = useSetRecoilState(userStats);
  const setIsAuthenticated = useSetRecoilState(isAuthenticatedState);
  const setUserCards = useSetRecoilState(userCardsStats);
  const setCards = useSetRecoilState(cardsStats);
  const setDeckSelection = useSetRecoilState(deckSelectionState);

  const authCheck = () => {
    http({
      type: "get",
      url: `/users/auth`,
      callback: (data:boolean) => setIsAuthenticated(data),
    });
  };

  const userLogin = (
    data:UserLogin,
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
      data: { data },
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

  const userSignUp = (
    data:UserSignUp,
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
      data: { data },
    });
  };

  const getUserStat = (onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/users/stat`,
      callback: (data:UserStat) => {
        setUser(data);
      },
      onError: onError,
      customSetLoading: setLoading,
    });
  };

  const updateUserStat = (
    data: UserStatUpdate,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "put",
      url: `/users/stat`,
      callback: (data:UserStat) => {
        setUser(data);
      },
      onError: onError,
      customSetLoading: setLoading,
      data: data,
    });
  };

  const getUserCards = (onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/users/cards`,
      callback: (data:UserCards) => {
        setUserCards(data);
      },
      onError: onError,
      customSetLoading: setLoading,
    });
  };

  const getUserDeckSelectionAll = (
    callback: (data: DeckSelection) => void,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "get",
      url: `/users/deck-selection`,
      callback: callback,
      onError: onError,
      customSetLoading: setLoading,
    });
  };

  const getUserDeckSelection = (
    mod_id: number,
    callback: (data: Deck) => void,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "get",
      url: `/users/deck-selection/${mod_id}`,
      callback: callback,
      onError: onError,
      customSetLoading: setLoading,
    });
  };

  const updateUserDeckSelection = (
    data: DeckSelectionUpdate,
    callback: (data: Deck) => void,
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
    userSignUp,
    getUserStat,
    updateUserStat,
    getUserCards,
    updateUserDeckSelection,
    getUserDeckSelection,
    getUserDeckSelectionAll
  };
};

export default useHttpUser;
