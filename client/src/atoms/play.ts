import { atom } from "recoil";
import { CardInfo, GameStat, PlayerStat } from "../types/games";

export const gameStatState = atom<GameStat>({
  key: "gameStat",
  default: {
    is_player_turn: false,
    trun: 0,
    side_effects: []
  }
})


export const playerStatState = atom<PlayerStat>({
  key: "playerStat",
  default: {
    health: 30,
    cost: 0,
    side_effects: []
  },
})

export const playerHandsState = atom<CardInfo[]>({
  key: "playerHands",
  default: [],
});

export const playerFieldsState = atom<Record<number, CardInfo | null>>({
  key: "playerFields",
  default: {
    0: null,
    1: null,
    2: null,
    3: null,
    4: null,
  },
});

export const playerGravesState = atom<CardInfo[]>({
  key: "playerGraves",
  default: [],
});

export const playerDecksState = atom<number>({
  key: "playerDecks",
  default: 40,
});
