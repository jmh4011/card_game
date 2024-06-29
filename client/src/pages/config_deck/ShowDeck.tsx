import { motion } from "framer-motion";
import React, { useState } from "react";
import styled from "styled-components";
import Card from "../../components/Card";
import { deck, player_card } from "../../utils/inter";

interface ShowDeckProps {
  deck: deck;
  setDeck: (data: any) => void;
  deckCards: player_card[];
  setDeckCards: (data: any) => void;
  setShowCard: (data: player_card) => void;
}

const ShowDeck: React.FC<ShowDeckProps> = ({ deck, setDeck, deckCards, setDeckCards, setShowCard }) => {
  const [isNameEditing, setIsNameEditing] = useState(false);
  const [cardToRemove, setCardToRemove] = useState<number | null>(null);

  const handleDeckCardRightClick = (e: React.MouseEvent, index: number) => {
    e.preventDefault();
    setCardToRemove(index);
    setTimeout(() => {
      setDeckCards((prev: any) => prev.filter((card: player_card, idx: number) => idx !== index));
      setCardToRemove(null);
    }, 300);
  };

  return (
    <DeckContainer>
      <DeckName onDoubleClick={() => setIsNameEditing(true)}>
        {isNameEditing ? (
          <EditNameInput
            type="text"
            defaultValue={deck.deck_name}
            onChange={(e) => setDeck((pre: any) => ({ ...pre, deck_name: e.target.value }))}
            onKeyDown={(e) => { if (e.key === 'Enter') setIsNameEditing(false); }}
            onBlur={() => setIsNameEditing(false)}
            autoFocus
          />
        ) : (
          deck.deck_name
        )}
      </DeckName>
      <CardList>
        {deckCards.map((value, idx) => (
          <CardWrapper
            key={idx}
            onClick={() => setShowCard(value)}
            onContextMenu={(e) => handleDeckCardRightClick(e, idx)}
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: cardToRemove === idx ? 0 : 1, y: cardToRemove === idx ? -20 : 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card card={value} scale={.15} />
          </CardWrapper>
        ))}
      </CardList>
    </DeckContainer>
  );
};

export default ShowDeck;

const DeckContainer = styled.div`
  float: left;
  border: 1px solid black;
  width: 35%;
  height: 80%;
  margin-top: 5%;
  margin-left: 3%;
`;

const DeckName = styled.div`
  border: 1px solid rgb(255, 1, 1);
`;

const EditNameInput = styled.input`
  outline: none;
  border-width: 0;
`;

const CardList = styled.div`
  border: 1px solid rgb(1, 0, 1);
  width: 100%;
  height: 80%;
  max-height: 80%;
  overflow-y: auto;
  gap: 10px;

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
  }

  &::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 10px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: #555;
  }
`;

const CardWrapper = styled(motion.div)`
  display: inline-block;
`;
