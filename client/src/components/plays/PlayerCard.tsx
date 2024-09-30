import React from "react";
import { useDrag } from "react-dnd";
import { CardInfo } from "../../types/games";

interface PlayerCardProps {
  card: CardInfo;
  index: number;
}

const PlayerCard: React.FC<PlayerCardProps> = ({ card, index }) => {
  const [, drag] = useDrag(() => ({
    type: "card",
    item: { index }
  }));

  return <div ref={drag}>{card.card_name}</div>;
};

export default PlayerCard;
