import { Card, Deck, Effect } from "./models";

export type CardCount = Record<number, number>;

export interface UserLogin {
  username: string
  password: string
}

export interface UserSignUp {
  username: string
  password: string
  again_password: string
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

export interface DeckCreate {
  deck_name: string;
  image_path: String;
}

export interface DeckUpdateReturn {
  deck: Deck;
  deck_cards: DeckCards;
}

export type UserCards = Record<number,number>

export type DeckCards = Record<number,number>

export type DeckSelection = Record<number, Deck>;


export interface DeckSelectionUpdate {
  deck_id: number;
  mod_id: number;
}



export interface CardRetrun {
  cards: Record<number, Card>;
  effects: Record<number, Effect>;
}