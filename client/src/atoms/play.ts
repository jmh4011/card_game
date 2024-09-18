import { atom } from "recoil";
import { CardInfo, GameStat, Player } from "../types/games";

export const gameStatState = atom<GameStat>({
  key: "gameStat",
  default: {
    is_player_turn: false,
    trun: 0,
    side_effects: []
  }
})

export const playerState = atom<Player>({
  key: 'playerState',
  default: {
    health: 30,
    cost: 0,
    side_effects: [],
    hands: [],
    fields: {
      0: null,
      1: null,
      2: null,
      3: null,
      4: null,
    },
    graves: [],
    decks: 40,
  },
});