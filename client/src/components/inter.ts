export interface d2 {
  x : number;
  y : number;
}

export interface phyObject_value {
  mess: number; 
  position: d2; 
  velocity: d2; 
  acceleration: d2;
  volume: d2
}

export interface phyObject {
  [name: string]: phyObject_value
}
