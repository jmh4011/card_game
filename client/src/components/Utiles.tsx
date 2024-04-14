import React,{ useEffect } from "react";
import { socket } from "../App";

export const styleVibration = (setVibration:(vibration:boolean)=>void,t:number = 400) => {
    setVibration(true);
    setTimeout(function() {
        setVibration(false);
    }, t);
  }


export const useSocketOn = (ev:string, callBack:(data:any)=>void, deps:React.DependencyList = []) => {
    useEffect(() => {

        socket.on(ev, data => {
            callBack(data);
        })
        
        return () => {
            socket.off(ev);
        };
    }, deps);
}