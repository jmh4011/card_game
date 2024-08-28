import { useSetRecoilState } from "recoil";
import { useHttp } from "./api";
import { cardsStats, decksState } from "../atoms/global";
import { SetFn } from "../utils/types";

const useHttpCard = () => {
  const { http } = useHttp();
  const setCards = useSetRecoilState(cardsStats);

  const getCards = (onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/cards`,
      callback: (data) => {
        setCards(data);
      },
      customSetLoading: setLoading,
      onError: onError,
    });
  };

  return { getCards };
};

export default useHttpCard;
