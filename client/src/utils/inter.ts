export interface card {
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

export interface skin {
  backgraund: string;
  character: string;
}


export interface deck {
  deck_id: number;
  player_id: number;
  deck_name: string;
  image: string;
}

export interface deck_card {
  deck_card_id: number;
  deck_id: number;
  card_id: number;
}


export interface player_card extends card{
  card_count: number
}

export interface player_stats {
  stat_id: number;
  player_id: number;
  current_deck_id: number | null;
  money: number;
}