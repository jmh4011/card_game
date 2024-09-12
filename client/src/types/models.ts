export interface Card {
  card_id: number;
  card_name: string;
  card_class: string;
  attack: number;
  health: number;
  effects: number[];
  image_path: string;
  card_type: number;
}


export interface Effect {
  effect_id: number;
  effect_name: string;
  condition: string | null;
  cost: string | null;
  effect: string | null; 
}

export interface Deck {
  deck_id: number;
  user_id: number;
  deck_name: string;
  image_path: string;
  is_public: boolean;
}


export interface GameMod {
  mod_id: number;
  mod_name: string;
  image_path: string;
  description: string;
  is_open: boolean;
}