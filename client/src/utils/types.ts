export type SetFn = (data: any) => void;

export type CardCount = Record<number,number>

export interface Card {
  card_id: number;
  card_name: string;
  card_class: string;
  attack: number;
  health: number;
  description: string;
  image: string;
  cost: number;
  card_type: number;
}

export interface Skin {
  backgraund: string;
  character: string;
}


export interface Deck {
  deck_id: number;
  player_id: number;
  deck_name: string;
  image: string;
}


export interface PlayerStats {
  stat_id: number;
  player_id: number;
  current_deck_id: number | null;
  money: number;
}

export interface DeckUpdate {
  deck_name: string;
  image: string;
  deck_cards: CardCount;
}