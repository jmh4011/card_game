import { useSetRecoilState } from "recoil";
import { useHttp } from "./http";
import {} from "../atoms/global";
import { SetFn } from "../types/types";
import { DeckCards, DeckCreate, DeckUpdate, DeckUpdateReturn } from "../types/routers";
import { Deck } from "../types/models";

const useHttpDeck = () => {
  const { http } = useHttp();

  const getDecks = (
    callback: (data: Deck[]) => void,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "get",
      url: `/decks`,
      callback: callback,
      customSetLoading: setLoading,
      onError,
    });
  };

  const getDeck = (
    deck_id: number,
    callback: (data: Deck[]) => void,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "get",
      url: `/decks/${deck_id}`,
      callback: callback,
      customSetLoading: setLoading,
      onError,
    });
  };

  const createDeck = (
    data: DeckCreate,
    callback: (data: Deck) => void,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "post",
      url: `/decks`,
      callback: callback,
      customSetLoading: setLoading,
      onError,
      data: data,
    });
  };

  const getDeckCards = (
    deck_id: number,
    callback: (data: DeckCards) => void,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "get",
      url: `/decks/cards/${deck_id}`,
      callback: callback,
      customSetLoading: setLoading,
      onError,
    });
  };

  const updateDeck = (
    deck_id: number,
    data: DeckUpdate,
    callback: (data: DeckUpdateReturn) => void,
    onError?: SetFn,
    setLoading?: SetFn
  ) => {
    http({
      type: "put",
      url: `/decks/${deck_id}`,
      callback: callback,
      customSetLoading: setLoading,
      onError,
      data,
    });
  };

  return { getDeck, getDecks, createDeck, getDeckCards, updateDeck };
};

export default useHttpDeck;
