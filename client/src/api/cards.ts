import { useSetRecoilState } from 'recoil';
import { useHttp } from './api';
import {  decksState } from '../atoms/global';
import { SetFn} from '../utils/types';

const useHttpCard = () => {
  const { http } = useHttp();

  const get = (callback:SetFn,onError?: SetFn, setLoading?: SetFn) => {
    http({
      type: "get",
      url: `/cards`,
      callback:callback,
      customSetLoading: setLoading,
      onError:onError
    });
  }



  return {get};
}

export default useHttpCard