import { atom } from "recoil";
import { CardCount, Deck} from "../utils/types";


export const deckState = atom<Deck>({
  key: 'deck',
  default: {deck_id:1,deck_name:'null',image_path:'0.png',user_id:0},
});


export const tempDeckState = atom<Deck>({
  key: 'tempDeck',
  default: {deck_id:1,deck_name:'null',image_path:'0.png',user_id:0},
});

export const deckCardsState = atom<CardCount>({
  key: 'deckCards',
  default: [],
});

export const tempDeckCardsState = atom<CardCount>({
  key: 'tempDeckCards',
  default: [],
})

export const showCardState = atom<number | null>({
  key: 'showCarde', 
  default: null,
});


export interface SearchSettings {
  search: string;
  order: 'Ascending' | 'Descending';
  stand: string;
  searchName: boolean;
  searchClass: boolean;
  searchDescription: boolean;
}


export const searchSettingsState = atom<SearchSettings>({
  key: 'searchSettings',
  default: {
    search: '',
    order: 'Ascending',
    stand: 'id',
    searchName: true,
    searchClass: false,
    searchDescription: false,
  },
});

export const showExitCheckState = atom<boolean>({
  key: 'showExitCheckState',
  default: false,
});
