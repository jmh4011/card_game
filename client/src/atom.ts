import React from "react";
import { Cookies } from "react-cookie";
import { atom } from "recoil";
import { deck } from "./utile/inter";

const cookies = new Cookies();


export const modalState = atom<{ id: string; element: React.FC }[]>({
  key: 'modalState',
  default: [],
});

export const userIdState = atom<number>({
  key: 'userId',
  default: Number(cookies.get('userId')) || 0,
})  

export const decksState = atom<deck[]>({
  key: 'decks',
  default: [],
})

export const showPageState = atom<"main" | "login" | 'createAccount' | "seletDeck">({
  key: 'showPage',
  default: cookies.get('userId')? "main": "login" ,
})

export const showDeckState = atom<number>({
  key: 'showDeck',
  default: 0,
})