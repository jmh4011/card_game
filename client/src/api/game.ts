import { useSetRecoilState } from 'recoil';
import { useHttp } from './api';
import { SetFn} from '../utils/types';

const useHttpGame = () => {
  const { http } = useHttp();

  const getModes = (callback:SetFn,onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/games/modes`,
      callback:callback,
      customSetLoading: setLoading,
      onError:onError
    });
  }

  const getToken = (callback:SetFn,onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/games/tokens`,
      callback:callback,
      customSetLoading: setLoading,
      onError:onError
    });
  }

  return {getModes, getToken};
}

export default useHttpGame