export type SetFn = (data: any) => void;

export type CardCount = Record<number,number>

export interface Card {
  card_id: number;
  card_name: string;
  card_class: string;
  attack: number;
  health: number;
  description: string;
  image_path: string;
  card_type: number;
}

export interface Skin {
  backgraund: string;
  character: string;
}


export interface Deck {
  deck_id: number;
  user_id: number;
  deck_name: string;
  image_path: string;
}


export interface UserStat {
  stat_id: number;
  user_id: number;
  nickname: string;
  money: number;
}

export interface DeckUpdate {
  deck_name: string;
  image_path: string;
  deck_cards: CardCount;
}

export type DeckSelection =  Record<string, number>

export interface DeckSelectionUpdate {
  deck_id: number;
  game_mode: string;
}