import { useEffect } from 'react';
import {Cookies} from 'react-cookie';
import { useRecoilValue } from 'recoil';
import { userIdState } from '../atom';

const cookies = new Cookies();

export const setCookie = (name: string, value: any, options?: any) => {
  cookies.set(name, value, { ...options });
}

export const getCookie = (name: string) => {
  return cookies.get(name);
}

export const removeCookie = (name: string, options?: any) => {
  cookies.remove(name, { ...options });
}

export const useUserIdSync = () => {
  const userId = useRecoilValue(userIdState);

  useEffect(() => {
    if (userId) {
      setCookie('userId', userId, { path: '/'});
    } else {
      removeCookie('userId', { path: '/' });
    }
  }, [userId]);
};
