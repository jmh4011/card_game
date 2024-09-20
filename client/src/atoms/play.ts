
// atoms/play.ts

import { atom } from 'recoil';
import { CardInfo, GameStat, Player } from '../types/games';


export const gameStatState = atom<GameStat>({
  key: "gameStat",
  default: {
    is_player_turn: false,
    turn: 0,
    side_effects: []
  }
})



export const playerHandsState = atom<CardInfo[]>({
  key: 'playerHands',
  default: [],
});

export const playerFieldsState = atom<Record<number, CardInfo | null>>({
  key: 'playerFields',
  default: {},
});

export const playerGravesState = atom<CardInfo[]>({
  key: 'playerGraves',
  default: [],
});

export const playerDecksState = atom<number>({
  key: 'playerDecks',
  default: 0,
});


export const playerState = atom<Player>({
  key: 'player',
  default: {
    cost: 0,
    health: 0,
    side_effects: []
  },
});