import React from "react";
import { useDrop, DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { CardInfo } from "../../types/games";

interface PlayerFieldUIProps {
  handleDrop: (index: number, cardIndex: number) => void;
  cards: CardInfo[];
}

const PlayerFieldUI: React.FC<PlayerFieldUIProps> = ({ handleDrop, cards }) => {
  const [, drop] = useDrop(() => ({
    accept: "card",
    drop: (item: any, monitor: any) => {
      const cardIndex = monitor.getItem().index;
      handleDrop(item.index, cardIndex);
    }
  }));

  return (
    <div ref={drop}>
      {cards.map((card, index) => (
        <div key={index}>{/* Custom card rendering */}</div>
      ))}
    </div>
  );
};

export default PlayerFieldUI;
