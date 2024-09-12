import { motion } from "framer-motion";
import React, { useState } from "react";
import styled, { css } from "styled-components";
import ShowCard from "../ShowCard";
import { useRecoilState, useRecoilValue, useSetRecoilState } from "recoil";
import { cardsStats, userCardsStats } from "../../atoms/global";
import { DeckCards } from "../../types/routers";
import { Deck } from "../../types/models";

interface ShowDeckPorps {
  readOnly: boolean;
  deck: Deck;
  setDeck?: (data: any) => void;
  deckCards: DeckCards;
  onCardClick: (value: number) => void;
  onCardContextMenu: (e: React.MouseEvent, value: number) => void;
}

const ShowDeck: React.FC<ShowDeckPorps> = ({
  readOnly,
  deck,
  setDeck,
  deckCards,
  onCardClick,
  onCardContextMenu,
}) => {
  const userCards = useRecoilValue(userCardsStats);
  const [isNameEditing, setIsNameEditing] = useState(false);
  const cards = useRecoilValue(cardsStats);

  return (
    <DeckContainer>
      <DeckName onDoubleClick={() => !readOnly && setIsNameEditing(true)}>
        {isNameEditing ? (
          <EditNameInput
            type="text"
            defaultValue={deck.deck_name}
            onChange={(e) =>
              setDeck &&
              setDeck((pre: any) => ({ ...pre, deck_name: e.target.value }))
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") setIsNameEditing(false);
            }}
            onBlur={() => setIsNameEditing(false)}
            autoFocus
          />
        ) : (
          deck.deck_name
        )}
      </DeckName>
      <CardList>
        {Object.entries(deckCards).flatMap(([key, value]) =>
          Array(value)
            .fill(Number(key))
            .map((cardId, index) => {
              const uniqueKey = `${cardId}-${index}`;
              const isExceedingUserCount = index >= (userCards[cardId] || 0);
              return (
                <CardWrapper
                  key={uniqueKey}
                  onClick={() => onCardClick(cardId)}
                  onContextMenu={(e) => onCardContextMenu(e, cardId)}
                  isExceedingUserCount={isExceedingUserCount}
                >
                  <ShowCard card={cards[cardId]} />
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
  width: 100%;
  height: 100%;
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
  box-sizing: border-box;
  max-height: 90%;
  overflow-y: auto;
  gap: 0.1%;

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

const CardWrapper = styled(motion.div).withConfig({
  shouldForwardProp: (prop) => prop !== "isExceedingUserCount",
})<{ isExceedingUserCount: boolean }>`
  display: inline-block;
  width: 20%;

  ${({ isExceedingUserCount }) =>
    isExceedingUserCount &&
    css`
      & * {
        opacity: 0.8;
      }
    `}
`;
