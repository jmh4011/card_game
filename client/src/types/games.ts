import { Card } from "./models";

// Enum 타입 정의
export type MessageType = "ping" | "text" |"game_info" |"action" | "move"

export type ZoneType = "hands" | "fields" | "graves" | "decks";

export type MoveType = "effect" | "attack" | "end";

export type ActionType =
  | "move"
  | "card_state"
  | "side_effect"
  | "cost"
  | "attack"
  | "destroy"
  | "damage"
  | "effect";

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

export interface Move {
  move_type: MoveType;
  entity: Entity;
  select: boolean;
  targets: Entity[];
  effect_id: number | null;
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
  fields: Record<number, CardInfo | null>;
  graves: CardInfo[];
  decks: number;
}

export interface Opponent {
  cost: number;
  health: number;
  side_effects: number[];
}

export interface GameInfo {
  player: PlayerInfo;
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
