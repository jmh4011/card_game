import { Card } from "./models";

// Enum 타입 정의
export type MessageType = "text" | "gameinfo" | "action";
export type ZoneType = "hand" | "field" | "grave" | "deck";
export type MoveType = "effect" | "attact" | "end";
export type ActionType =
  | "drow"
  | "attack"
  | "destroy"
  | "move"
  | "summon"
  | "damege"
  | "effect";
export type EntityZoneType = "hand" | "field" | "grave" | "deck" | "player";

// MessageModel 타입 정의
export interface MessageModel {
  type: MessageType;
  data: any; 
}

// Entity 타입 정의
export interface Entity {
  zone: EntityZoneType;
  index: number;
  opponent: boolean;
}

// CardInfo 타입 정의
export interface CardInfo extends Card {
  zone: ZoneType;
  index: number;
  opponent: boolean;
  side_effects: number[];
}

// MoveEffect 타입 정의
export interface MoveEffect {
  move_id: number;
  entity: Entity;
  effect_id: number;
  select: boolean;
  targets: Entity[];
}

// MoveAttack 타입 정의
export interface MoveAttack {
  move_id: number;
  entity: Entity;
  select: boolean;
  targets: Entity[];
}

// Move 타입 정의
export interface Move {
  effects: MoveEffect[];
  attact: MoveAttack[]; 
  end: boolean;
}

// MoveReturn 타입 정의
export interface MoveReturn {
  move_type: MoveType;
  move_id: number;
  target: number[];
}

// PlayerInfo 타입 정의
export interface PlayerInfo {
  cost: number;
  health: number;
  side_effects: number[];
  hands: CardInfo[];
  fields: Record<number , CardInfo>;
  graves: CardInfo[];
  decks: number;
}

// GameStat 타입 정의
export interface GameInfo {
  Player: PlayerInfo;
  opponent: PlayerInfo;
  trun: number;
  is_player_turn: boolean;
  side_effects: number[];
}

// Action 타입 정의
export interface Action {
  action_type: ActionType;
  subject: Entity;
  object: Entity;
  subject_state: CardInfo | PlayerInfo;
  object_state: CardInfo | PlayerInfo;
}

export interface GameStat {
  trun: number;
  is_player_turn: boolean;
  side_effects: number[];
}

export interface PlayerStat {
  health: number
  cost: number
  side_effects: number[];
}
