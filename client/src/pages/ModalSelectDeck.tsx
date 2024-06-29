import React, { useState, useEffect } from "react";
import { useRecoilState, useRecoilValue, useSetRecoilState } from "recoil";
import { PostDecks, GetDeckPlayerCards } from "../api/api";
import { deckCardsState, decksState, loadingState, showDeckState, showPageState, userIdState } from "../recoli/atom";
import styled from "styled-components";
import { deck } from "../utils/inter";

const ModalSelectDeck: React.FC = () => {
  const userId = useRecoilValue(userIdState);
  const [decks, setDecks] = useRecoilState(decksState);
  const [scale, setScale] = useState(0.4);
  const setShowPage = useSetRecoilState(showPageState);
  const setShowDeck = useSetRecoilState(showDeckState);
  const setDeckCards = useSetRecoilState(deckCardsState);
  const [loading, setLoading] = useRecoilState(loadingState);

  const handleCreate = () => {
    PostDecks(userId, (data: any) => {
      setDecks((prev: any) => [...prev, data]);
    }, setLoading);
  };

  const handleClick = (deck: deck) => {
    setShowDeck(deck);
    GetDeckPlayerCards(deck.deck_id, userId, setDeckCards, setLoading);
    setShowPage("configDeck");
  };

  return (
    <Container>
      {decks.map((value, idx) => (
        <Deck key={idx} scale={scale} onClick={() => handleClick(value)}>
          <DeckImg src={`/static/images/character/1.png`} scale={scale} />
          <DeckName scale={scale}>{value.deck_name}</DeckName>
        </Deck>
      ))}
      <CreateButton onClick={handleCreate}>Create Deck</CreateButton>
    </Container>
  );
};

export default ModalSelectDeck;

const Container = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  padding: 20px;
`;

const Deck = styled.div<{ scale: number }>`
  margin: 5vh 5vw;
  display: inline-block;
  width: ${({ scale }) => 600 * scale}px;
  height: ${({ scale }) => 600 * scale}px;
  border: 1px solid rgb(0, 0, 0);
  text-align: center;
  cursor: pointer;
`;

const DeckImg = styled.img<{ scale: number }>`
  width: ${({ scale }) => 560 * scale}px;
  height: ${({ scale }) => 380 * scale}px;
`;

const DeckName = styled.div<{ scale: number }>`
  font-size: ${({ scale }) => 140 * scale}px;
`;

const CreateButton = styled.button`
  width: 200px;
  height: 50px;
  background-color: rgb(0, 150, 255);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;

  &:hover {
    background-color: rgb(0, 120, 200);
  }
`;
