import React from "react";
import { Cookies } from "react-cookie";
import { atom } from "recoil";
import { card, deck, player_card, player_stats } from "../utils/inter";

const cookies = new Cookies();


export const modalState = atom<{ id: string; element: React.FC }[]>({
  key: 'modalState',
  default: [],
});

export const loadingState = atom<boolean>({
  key: 'loading',
  default: false,
})

export const userIdState = atom<number>({
  key: 'userId',
  default: Number(cookies.get('userId')) || 0,
})  

export const playerStats = atom<player_stats>({
  key: 'player',
  default: {stat_id:0, player_id:0, current_deck_id: null, money:0}
})

export const playerCardsStats = atom<player_card[]>({
  key:  'playerCrads',
  default: []
})

export const decksState = atom<deck[]>({
  key: 'decks',
  default: [],
})


export const showPageState = atom<'start' |"main" | "login" | 'createAccount' | "selectDeck" | "configDeck">({
  key: 'showPage',
  default: cookies.get('userId')? "start": "login" ,
})

export const showDeckState = atom<deck>({
  key: 'showDeck',
  default: {deck_id:1,deck_name:'null',image:'0.png',player_id:0},
})

export const deckCardsState = atom<player_card[]>({
  key: 'deckCards',
  default: [],
})