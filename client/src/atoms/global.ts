import React from "react";
import { atom } from "recoil";
import { Card, CardCount, Deck, UserStats } from "../utils/types";
import {ShowPage} from "../App"


export const modalState = atom<{ id: string; element: React.FC }[]>({
  key: 'modalState',
  default: [],
});


export const loadingState = atom<boolean>({
  key: 'loading',
  default: false,
})

export const userStats = atom<UserStats>({
  key: 'user',
  default: {stat_id:0, user_id:0, current_deck_id: null, money:0}
})

export const cardsStats = atom<Record<number, Card>>({
  key: 'cards',
  default: {}
})


export const userCardsStats = atom<CardCount>({
  key:  'userCrads',
  default: {}
})

export const decksState = atom<Deck[]>({
  key: 'decks',
  default: [],
})

export const showPageState = atom<ShowPage>({
  key: 'showPage',
  default: "login" ,
})