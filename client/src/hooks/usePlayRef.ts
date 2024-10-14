import { useRef } from "react";
import { Entity } from "../types/games";

export const usePlayRef = () => {
  const playerHandRefs = useRef([]);
  const playerFieldRefs = useRef([]);
  
  const opponentHandRefs = useRef([]);
  const opponentFieldRefs = useRef([]);

  const getCardRef = (entity: Entity): React.RefObject<HTMLDivElement> | null => {
    if (entity.opponent) {
    
      switch (entity.zone) {
        case 'hands':
          return opponentHandRefs.current[entity.index] || null;
        case 'fields':
          return opponentFieldRefs.current[entity.index] || null;
        default:
          return null;
      }
    
    }
  
    switch (entity.zone) {
      case 'hands':
        return playerHandRefs.current[entity.index] || null;
      case 'fields':
        return playerFieldRefs.current[entity.index] || null;
      default:
        return null;
    }
  };
  
  return {
    getCardRef
  }
}

