import { useSetRecoilState } from "recoil";
import { useHttp } from "./api";
import { SetFn } from "../utils/types";

const useHttpGame = () => {
  const { http } = useHttp();

  const getMods = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/games/mods`,
      callback: callback,
      customSetLoading: setLoading,
      onError: onError,
    });
  };

  const getToken = (callback: SetFn, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/games/tokens`,
      callback: callback,
      customSetLoading: setLoading,
      onError: onError,
    });
  };

  return { getMods, getToken };
};

export default useHttpGame;
