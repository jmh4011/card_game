import React from "react";
import styled from "styled-components";
import ShowCard from "../ShowCard";
import { useDrag, useDrop, DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { Card } from "../../types/models";
import { CardInfo } from "../../types/games";
import { usePlayerFieldState } from "../../hooks/usePlayerFieldState";

interface PlayerFieldProps {
  handleCard: (val: CardInfo) => void;
  handleDrop: (index: number, cardIndex: number) => void;
}

const PlayerField: React.FC<PlayerFieldProps> = ({
  handleCard,
  handleDrop,
}) => {
  const { hands, fields, graves, decks } = usePlayerFieldState();



  return (
    <DndProvider backend={HTML5Backend}>
      <Contener>
        <Player>나</Player>
        <Fields>
          {[0, 1, 2, 3, 4].map((idx) => (
            <DroppableFieldCard
              key={idx}
              index={idx}
              card={fields[idx]}
              onDrop={handleDrop}
            />
          ))}
        </Fields>
        <Hands>
          {hands.map((val, idx) => (
            <DraggableHandCard
              key={idx}
              index={idx}
              total={hands.length}
              card={val}
              onClick={() => handleCard(val)}
            />
          ))}
        </Hands>
        <Graves>{graves.length}</Graves>
        <Deck>{decks}</Deck>
      </Contener>
    </DndProvider>
  );
};

export default PlayerField;

// 드래그 가능한 HandCard 컴포넌트
const DraggableHandCard: React.FC<{
  card: Card;
  index: number;
  total: number;
  onClick: () => void;
}> = ({ card, index, total, onClick }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: "card",
    item: { index },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  return (
    <HandCard
      ref={drag}
      $index={index}
      $total={total}
      onClick={onClick}
      $isDragging={isDragging}
    >
      <ShowCard card={card} />
    </HandCard>
  );
};

// 드롭 가능한 FieldCard 컴포넌트
const DroppableFieldCard: React.FC<{
  index: number;
  card: Card | null;
  onDrop: (index: number, cardIndex: number) => void;
}> = ({ index, card, onDrop }) => {
  const [{ isOver, canDrop }, drop] = useDrop(() => ({
    accept: "card",
    drop: (item: { index: number }) => onDrop(index, item.index),
    collect: (monitor) => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop(),
    }),
  }));

  return (
    <FieldCard ref={drop} $isOver={isOver} $canDrop={canDrop}>
      {isOver && !card && <Overlay />}
      {card && <ShowCard card={card} />}
    </FieldCard>
  );
};

// 스타일 정의
const Contener = styled.div`
  width: 100%;
  height: 100%;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  box-sizing: border-box;
`;

const Deck = styled.div`
  position: absolute;
  display: flex;
  right: 0;
  bottom: 0;
  height: 45%;
  aspect-ratio: 3 / 4;
  align-items: center;
  justify-content: center;
  border: 1px solid rgb(0, 0, 0);
`;

const Graves = styled.div`
  position: absolute;
  display: flex;
  right: 0;
  top: 0;
  height: 45%;
  aspect-ratio: 3 / 4;
  align-items: center;
  justify-content: center;
  border: 1px solid rgb(0, 0, 0);
`;

const HandCard = styled.div<{
  $index: number;
  $total: number;
  $isDragging: boolean;
}>`
  position: relative;
  display: flex;
  height: 20vh;
  aspect-ratio: 3 / 4;
  box-sizing: border-box;
  flex-shrink: 0;
  transition: transform 0.3s ease, z-index 0.3s ease;
  opacity: ${({ $isDragging }) => ($isDragging ? 0.5 : 1)};
  &:not(:first-child) {
    margin-left: ${({ $total }) => ($total > 8 ? "-8vw" : "-4vw")};
  }

  &:hover {
    transform: scale(1.5);
  }

  ${({ $isDragging }) =>
    $isDragging &&
    `
    transform: scale(1.1);
  `}
`;

const Hands = styled.div`
  position: absolute;
  display: flex;
  left: 50%;
  bottom: -8vh;
  transform: translate(-50%);
  justify-content: flex-end;
  border: 1px solid rgb(0, 0, 0);
  padding: 10px 0;
`;

const Player = styled.div`
  position: absolute;
  display: flex;
  left: 0;
  bottom: 0;
  width: 15vw;
  height: 15vh;
  align-items: center;
  justify-content: center;
  border: 1px solid rgb(0, 0, 0);
`;

const Fields = styled.div`
  position: absolute;
  display: flex;
  left: 50%;
  top: 0;
  transform: translate(-50%);
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
  border: 1px solid rgb(0, 0, 0);
  gap: 10px;
`;

const FieldCard = styled.div<{ $isOver: boolean; $canDrop: boolean }>`
  display: flex;
  width: 10vw;
  aspect-ratio: 3 / 4;
  border: 1px solid ${({ $isOver }) => ($isOver ? "blue" : "rgb(100, 0, 0)")};
  box-sizing: border-box;
  flex-shrink: 1;
  transition: transform 0.3s ease;
  position: relative;

  ${({ $isOver }) =>
    $isOver &&
    `
    transform: scale(1.1); /* 필드 위로 드래그할 때 살짝 확대 */
  `}
`;

const Overlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 255, 0.1); /* 드래그 중일 때 배경색 */
  pointer-events: none;
  z-index: 1;
`;
