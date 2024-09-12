import { useSetRecoilState } from "recoil";
import { useHttp } from "./api";

import { GameMod } from "../types/models";
import { SetFn } from "../types/types";

const useHttpGame = () => {
  const { http } = useHttp();

  const getMods = (callback: (data:GameMod[]) => void, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/games/mods`,
      callback: callback,
      customSetLoading: setLoading,
      onError: onError,
    });
  };

  const getMod = (mod_id: number, callback: (data:GameMod) => void, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/games/mods/${mod_id}`,
      callback: callback,
      customSetLoading: setLoading,
      onError: onError,
    });
  };

  const getToken = (callback: (data:string) => void, onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/games/tokens`,
      callback: callback,
      customSetLoading: setLoading,
      onError: onError,
    });
  };

  return {getMod, getMods, getToken };
};

export default useHttpGame;
