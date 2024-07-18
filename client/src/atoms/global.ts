import React from "react";
import { atom } from "recoil";
import { Card, CardCount, Deck, PlayerStats } from "../utils/types";
import {ShowPage} from "../App"


export const modalState = atom<{ id: string; element: React.FC }[]>({
  key: 'modalState',
  default: [],
});


export const loadingState = atom<boolean>({
  key: 'loading',
  default: false,
})

export const playerStats = atom<PlayerStats>({
  key: 'player',
  default: {stat_id:0, player_id:0, current_deck_id: null, money:0}
})

export const cardsStats = atom<Record<number, Card>>({
  key: 'cards',
  default: {}
})


export const playerCardsStats = atom<CardCount>({
  key:  'playerCrads',
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