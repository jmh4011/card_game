import axios, { AxiosResponse } from 'axios';
import { useSetRecoilState } from 'recoil';
import { loadingState, showPageState } from '../atoms/global';
import { SetFn } from '../utils/types';

interface HttpOptions {
  type: "get" | "put" | "post" | "delete";
  url: string;
  callback: SetFn;
  onError?: SetFn;
  customSetLoading?: SetFn;
  data?: any;
}

export const useHttp = () => {
  const setLoadingRecoil = useSetRecoilState(loadingState);
  const setShowPage = useSetRecoilState(showPageState);

  const http = async ({
    type,
    url,
    callback,
    onError,
    customSetLoading,
    data
  }: HttpOptions) => {
    const setLoading = customSetLoading ?? setLoadingRecoil;

    setLoading(true);

    const request = 
      type === 'get' ? axios.get : 
      type === 'put' ? axios.put : 
      type === 'post' ? axios.post : 
      axios.delete;

    try {
      const response: AxiosResponse = data === undefined ? 
        await request(url) : await request(url, data);
      console.log(response.data)
      callback(response.data);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('Error response:', error.response);
        console.error('Detail:', error.response?.data?.detail);

        if (error.response?.status === 401) {
          alert("세션이 만료되었습니다.");
          setShowPage("login");
        } else {
          if(onError)
          onError(error);
        }
      } else {
        console.error('Unexpected error:', error);
        if(onError)
        onError(error);
      }
    } finally {
      setLoading(false);
    }
  };

  return { http };
};
