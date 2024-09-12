import { useSetRecoilState } from "recoil";
import { useHttp } from "./api";
import { cardsStats, effectsStats} from "../atoms/global";
import { SetFn } from "../types/types";
import { CardRetrun } from "../types/routers";

const useHttpCard = () => {
  const { http } = useHttp();
  const setCards = useSetRecoilState(cardsStats);
  const setEffects = useSetRecoilState(effectsStats);

  const getCards = (onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/cards`,
      callback: (data:CardRetrun) => {
        setCards(data.cards);
        setEffects(data.effects)
      },
      customSetLoading: setLoading,
      onError: onError,
    });
  };

  return { getCards };
};

export default useHttpCard;
