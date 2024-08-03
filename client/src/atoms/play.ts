import { atom } from "recoil";
import { PlayMod } from "../pages/play/PlayPage";


export const playModState = atom<PlayMod>({
  key: "playMod",
  default: null
})

export const playDeckState = atom<number | null>({
  key: 'playDeck',
  default: null
})