import { useSetRecoilState } from "recoil";
import { useHttp } from "./api";
import { cardsStats, effectsStats} from "../atoms/global";
import { SetFn } from "../utils/types";

const useHttpCard = () => {
  const { http } = useHttp();
  const setCards = useSetRecoilState(cardsStats);
  const setEffects = useSetRecoilState(effectsStats);

  const getCards = (onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/cards`,
      callback: (data) => {
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
