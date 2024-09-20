// utils/playerStateUtils.ts

import { useRecoilState } from 'recoil';
import {
  playerHandsState,
  playerFieldsState,
  playerGravesState,
  playerDecksState,
  playerState,
} from '../atoms/play';
import { CardInfo, Entity } from '../types/games';

export const usePlayerStateActions = () => {
  const [player, setPlayer] = useRecoilState(playerState);
  const [hands, setHands] = useRecoilState(playerHandsState);
  const [fields, setFields] = useRecoilState(playerFieldsState);
  const [graves, setGraves] = useRecoilState(playerGravesState);
  const [decks, setDecks] = useRecoilState(playerDecksState);

  const setCost = (cost: number | ((prevCost: number) => number)) => {
    setPlayer((prevPlayer) => ({
      ...prevPlayer,
      cost: typeof cost === 'function' ? cost(prevPlayer.cost) : cost,
    }));
  };

  const setHealth = (health: number | ((prevHealth: number) => number)) => {
    setPlayer((prevPlayer) => ({
      ...prevPlayer,
      health: typeof health === 'function' ? health(prevPlayer.health) : health,
    }));
  };

  const setSideEffects = (
    sideEffects: number[] | ((prevEffects: number[]) => number[])
  ) => {
    setPlayer((prevPlayer) => ({
      ...prevPlayer,
      side_effects:
        typeof sideEffects === 'function'
          ? sideEffects(prevPlayer.side_effects)
          : sideEffects,
    }));
  };

  const removeCardFromZone = (entity:Entity) => {
    switch (entity.zone) {
      case 'fields':
        setFields((prevFields) => ({
          ...prevFields,
          [entity.index]: null,
        }));
        break;
      case 'hands':
        setHands((prevHands) => {
          const newHands = [...prevHands];
          newHands.splice(entity.index, 1);
          return newHands;
        });
        break;
      case 'graves':
        setGraves((prevGraves) => {
          const newGraves = [...prevGraves];
          newGraves.splice(entity.index, 1);
          return newGraves;
        });
        break;
      // 다른 존(zone)에 대한 처리도 필요하면 추가
    }
  };

  const addCardToZone = (entity:Entity, card: CardInfo) => {
    switch (entity.zone) {
      case 'fields':
        setFields((prevFields) => ({
          ...prevFields,
          [entity.index]: card,
        }));
        break;
      case 'hands':
        setHands((prevHands) => {
          const newHands = [...prevHands];
          newHands.splice(entity.index, 0, card);
          return newHands;
        });
        break;
      case 'graves':
        setGraves((prevGraves) => {
          const newGraves = [...prevGraves];
          newGraves.splice(entity.index, 0, card);
          return newGraves;
        });
        break;
      // 다른 존(zone)에 대한 처리도 필요하면 추가
    }
  };

  const updateCardInZone = (entity: Entity, card: CardInfo) => {
    switch (entity.zone) {
      case 'fields':
        setFields((prevFields) => ({
          ...prevFields,
          [entity.index]: card,
        }));
        break;
      case 'hands':
        setHands((prevHands) => {
          const newHands = [...prevHands];
          newHands[entity.index] = card;
          return newHands;
        });
        break;
      case 'graves':
        setGraves((prevGraves) => {
          const newGraves = [...prevGraves];
          newGraves[entity.index] = card;
          return newGraves;
        });
        break;
      // 다른 존(zone)에 대한 처리도 필요하면 추가
    }
  };

  return {
    player,
    hands,
    fields,
    graves,
    decks,
    setHands,
    setFields,
    setGraves,
    setPlayer,
    setDecks,
    setCost,
    setHealth,
    setSideEffects,
    removeCardFromZone,
    addCardToZone,
    updateCardInZone,
  };
};
