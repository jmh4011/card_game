import { useSetRecoilState } from 'recoil';
import { useHttp } from './api';
import {  decksState } from '../atoms/global';
import { SetFn} from '../utils/types';

const useHttpCard = () => {
  const { http } = useHttp();

  const getCards = (callback:SetFn,onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/cards`,
      callback:callback,
      customSetLoading: setLoading,
      onError:onError
    });
  }



  return {getCards};
}

export default useHttpCard