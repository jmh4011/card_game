import { atom } from "recoil";
import { CardInfo } from "../types/games";

export const playerState = atom

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
  key: "playerHands",
  default: 40,
});
