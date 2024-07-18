import { atom } from "recoil";
import { PlayMod } from "../pages/modals/ModalPlay";


export const playModState = atom<PlayMod>({
  key: "playMod",
  default: "test"
})