import axios, { AxiosResponse } from 'axios';

type setFn = (data: any) => void;

export const http = async (
  type: "get" | "put" | "post" | "delete",
  url: string,
  callback: (data: any) => void,
  setLoading: setFn,
  data: any = undefined) => {
  
  setLoading(true);
  
  const request = 
  type === 'get' ? axios.get : 
  type === 'put' ? axios.put : 
  type === 'post'? axios.post: 
  axios.delete;

  try {
    const response: AxiosResponse = data === undefined 
      ? await request(url) 
      : await request(url, data);
    callback(response.data);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Error response:', error.response);
      console.error('Detail:', error.response?.data?.detail);
    } else {
      console.error('Unexpected error:', error);
    }
  } finally {
    setLoading(false);
  }
}
