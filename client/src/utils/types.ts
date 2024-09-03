export type SetFn = (data: any) => void;

export type CardCount = Record<number, number>;

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
  is_public: boolean;
}

export interface UserStat {
  stat_id: number;
  user_id: number;
  nickname: string;
  money: number;
  current_mod_id: number;
}

export interface UserStatUpdate {
  nickname: string | null;
  money: number | null;
  current_mod_id: number | null;
}

export interface DeckUpdate {
  deck_name: string;
  image_path: string;
  is_public: boolean;
  deck_cards: CardCount;
}

export type DeckSelection = Record<string, number>;

export interface DeckSelectionUpdate {
  deck_id: number;
  mod_id: number;
}

export interface GameMod {
  mod_id: number;
  mod_name: string;
  image_path: string;
  description: string;
  is_open: boolean;
}
