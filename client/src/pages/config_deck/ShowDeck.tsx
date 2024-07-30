import { motion } from "framer-motion";
import React, { useState } from "react";
import styled, { css } from "styled-components";
import Card from "../../components/Card";
import { useRecoilState, useRecoilValue, useSetRecoilState } from "recoil";
import { showCardState, tempDeckCardsState, tempDeckState } from "../../atoms/modalConfigDeck";
import { playerCardsStats } from "../../atoms/global";

const ShowDeck: React.FC = () => {
  const [deck, setDeck] = useRecoilState(tempDeckState);
  const [deckCards, setDeckCards] = useRecoilState(tempDeckCardsState);
  const playerCards = useRecoilValue(playerCardsStats);
  const setShowCard = useSetRecoilState(showCardState);

  const [isNameEditing, setIsNameEditing] = useState(false);
  const [cardToRemove, setCardToRemove] = useState<string | null>(null);

  const handleDeckCardRightClick = (e: React.MouseEvent, value: number, uniqueKey: string) => {
    e.preventDefault();
    setCardToRemove(uniqueKey);
    setTimeout(() => {
      setDeckCards((prev: any) => {
        const newState = { ...prev };
        if (newState[value] !== undefined) {
          newState[value] -= 1;
          if (newState[value] === 0) {
            delete newState[value];
          }
        }
        return newState;
      });
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
        {Object.entries(deckCards).flatMap(([key, value]) =>
          Array(value).fill(Number(key)).map((cardId, index) => {
            const uniqueKey = `${cardId}-${index}`;
            const isExceedingPlayerCount = index >= (playerCards[cardId] || 0);
            return (
              <CardWrapper
                key={uniqueKey}
                onClick={() => setShowCard(cardId)}
                onContextMenu={(e) => handleDeckCardRightClick(e, cardId, uniqueKey)}
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: cardToRemove === uniqueKey ? 0 : 1, y: cardToRemove === uniqueKey ? -20 : 0 }}
                transition={{ duration: 0.5 }}
                isExceedingPlayerCount={isExceedingPlayerCount}
              >
                <Card card_id={cardId}/>
              </CardWrapper>
            );
          })
        )}
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
  height: 90%;
  max-height: 90%;
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

const CardWrapper = styled(motion.div).withConfig({shouldForwardProp: (prop) => prop !== 'isExceedingPlayerCount'})<{ isExceedingPlayerCount: boolean }>`
  display: inline-block;
  width: 10%;

  ${({ isExceedingPlayerCount }) =>
    isExceedingPlayerCount &&
    css`
      & * {
        opacity: 0.8;
      }
    `}
`;
