import { ActionType, Entity, CardInfo } from "./games"

export interface Action {
  action_type: ActionType
  action_data: any
}
export interface ActionMove {
  before: Entity
  after: Entity
}
export interface ActionCardState {
  entity: Entity
  state: CardInfo
}
export interface ActionSideEffect {
  entity: Entity
  effect: number
}
export interface ActionCost {
  cost: number
}
export interface ActionEffect {
  effect: number
  subject: Entity
  targets: Entity[]
}
export interface ActionAttack {
  subject: Entity
  object: Entity
}
export interface ActionDestroy {
  entity: Entity
}
export interface ActionDamage {
  entity: Entity
  damage: number
}