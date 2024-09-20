import { Card } from "./models";

// Enum 타입 정의
export type MessageType = "text" | "game_info" | "action";
export type ZoneType = "hands" | "fields" | "graves" | "decks";
export type MoveType = "effect" | "attact" | "end";
export type ActionType =
| "move"
| "card_state"
| "side_effect"
| "cost"
| "attack"
| "destroy"
| "damage"
| "effect"
export type EntityZoneType = "hands" | "fields" | "graves" | "decks" | "player";

export interface MessageModel {
  type: MessageType;
  data: any; 
}

export interface Entity {
  zone: EntityZoneType;
  index: number;
  opponent: boolean;
}

export interface CardInfo extends Card {
  side_effects: number[];
}

export interface MoveEffect {
  move_id: number;
  entity: Entity;
  effect_id: number;
  select: boolean;
  targets: Entity[];
}

export interface MoveAttack {
  move_id: number;
  entity: Entity;
  select: boolean;
  targets: Entity[];
}

export interface Move {
  effects: MoveEffect[];
  attact: MoveAttack[]; 
  end: boolean;
}

export interface MoveReturn {
  move_type: MoveType;
  move_id: number;
  target: number[];
}

export interface PlayerInfo {
  cost: number;
  health: number;
  side_effects: number[];
  hands: CardInfo[];
  fields: Record<number , CardInfo | null>;
  graves: CardInfo[];
  decks: number;
}

export interface Opponent {
  cost: number;
  health: number;
  side_effects: number[];

}

export interface GameInfo {
  Player: PlayerInfo;
  opponent: PlayerInfo;
  turn: number;
  is_player_turn: boolean;
  side_effects: number[];
}


export interface GameStat {
  turn: number;
  is_player_turn: boolean;
  side_effects: number[];
}

export interface Player {
  cost: number;
  health: number;
  side_effects: number[];
}
