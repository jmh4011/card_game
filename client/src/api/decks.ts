import { useSetRecoilState } from "recoil";
import { useHttp } from "./api";
import {} from "../atoms/global";
import { SetFn, DeckUpdate } from "../utils/types";

const useHttpDeck = () => {
  const { http } = useHttp();

  const getDecks = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
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
    callback: SetFn,
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
    callback: SetFn,
    onError?: SetFn,
    setLoading?: SetFn,
    deck_name: string = `새로운 덱`,
    image: string = "0.png"
  ) => {
    http({
      type: "post",
      url: `/decks`,
      callback: callback,
      customSetLoading: setLoading,
      onError,
      data: { deck_name, image },
    });
  };

  const getDeckCards = (
    deck_id: number,
    callback: SetFn,
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
    callback: SetFn,
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
