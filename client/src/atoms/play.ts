import { atom } from "recoil";
import { ShowPlayPage } from "../pages/play/PlayPage";

export const showPagePlayState = atom<ShowPlayPage>({
  key: "showPlayPage",
  default: "home",
});
