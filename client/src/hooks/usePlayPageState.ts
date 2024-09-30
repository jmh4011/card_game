import { useState } from 'react';
import { useRecoilState } from 'recoil';
import { gameStatState } from '../atoms/play';
import { CardInfo } from '../types/games';

export const usePlayPageState = () => {
  const [showCardInfo, setShowCardInfo] = useState<CardInfo | null>(null);
  const [gameStat, setGamestat] = useRecoilState(gameStatState);

  const updateCardInfo = (card: CardInfo) => {
    setShowCardInfo(card);
  };

  return {
    showCardInfo,
    gameStat,
    setGamestat,
    updateCardInfo,
  };
};
