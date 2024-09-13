import axios, { AxiosResponse } from "axios";
import { useSetRecoilState } from "recoil";
import { loadingState } from "../atoms/global";
import { useNavigate } from "react-router-dom";
import { SetFn } from "../types/types";

interface HttpOptions {
  type: "get" | "put" | "post" | "delete";
  url: string;
  callback: SetFn;
  onError?: SetFn;
  customSetLoading?: SetFn;
  data?: any;
}

const api = axios.create({
  baseURL: "/api",
  headers: {},
});

export const useHttp = () => {
  const setLoadingRecoil = useSetRecoilState(loadingState);
  const navigate = useNavigate();
  
  const _http = async ({
    type,
    url,
    callback,
    onError,
    customSetLoading,
    data,
  }: HttpOptions) => {
    const setLoading = customSetLoading ?? setLoadingRecoil;

    setLoading(true);

    const request =
      type === "get"
        ? api.get
        : type === "put"
        ? api.put
        : type === "post"
        ? api.post
        : api.delete;

    try {
      const response: AxiosResponse =
        data === undefined ? await request(url) : await request(url, data);
      // console.log(response.data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Error response:", error.response);
        console.error("Detail:", error.response?.data?.detail);
        if (error.response?.data?.detail === "User Unauthorized") {
          navigate("/login");
        }

        if (onError) onError(error);

        // if (error.response?.status === 401) {
        //   alert("세션이 만료되었습니다.");
        //   setShowPage("login");
        // } else {
        // }
      } else {
        console.error("Unexpected error:", error);
        // if(onError)
        // onError(error);
      }
    } finally {
      setLoading(false);
    }
  };

  const http = async ({
    type,
    url,
    callback,
    onError,
    customSetLoading,
    data,
  }: HttpOptions) => {
    const result = await _http({
      type: type,
      url: url,
      callback: (data) => {},
      onError: onError,
      customSetLoading:customSetLoading,
      data:data
    });
    console.log(result)
    if(result !== undefined){
      
      callback(result);
    }
  };

  return { http };
};