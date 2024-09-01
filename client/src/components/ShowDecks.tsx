import React, { useEffect, useState } from "react";
import { useRecoilState } from "recoil";
import useHttpDeck from "../api/decks";
import styled from "styled-components";
import { Deck } from "../utils/types";
import { characterImage } from "../api/static";

interface ShowDecksPorps {
  handleDeckClick: (deck: Deck) => void;
  createButton: boolean;
}

const ShowDecks: React.FC<ShowDecksPorps> = ({
  handleDeckClick,
  createButton,
}) => {
  const { getDecks, createDeck } = useHttpDeck();
  const [decks, setDecks] = useState<Deck[]>([]);

  const handleCreate = () => {
    createDeck((data) => {
      setDecks((prev) => [...prev, data]);
    });
  };

  useEffect(() => {
    getDecks((data) => {
      setDecks(data);
    });
  }, []);

  return (
    <Modal>
      <Container>
        {decks.map((value, idx) => (
          <DeckContainer key={idx} onClick={() => handleDeckClick(value)}>
            <DeckImg src={characterImage(value.image_path)} />
            <DeckName>{value.deck_name}</DeckName>
          </DeckContainer>
        ))}
        {createButton && (
          <CreateButton onClick={handleCreate}>Create Deck</CreateButton>
        )}
      </Container>
    </Modal>
  );
};

export default ShowDecks;

const Modal = styled.div`
  width: 100%;
  height: 80%;
`;

const Container = styled.div`
  padding: 10px;
`;

const DeckContainer = styled.div`
  margin-left: 10px;
  display: inline-block;
  width: 15%;
  height: 40%;
  border: 1px solid rgb(0, 0, 0);
  text-align: center;
  cursor: pointer;
`;

const DeckImg = styled.img`
  height: 100%;
  width: 100%;
`;

const DeckName = styled.div`
  font-size: 30px;
  border: 1px solid rgb(0, 0, 0);
`;

const CreateButton = styled.button`
  width: 200px;
  height: 50px;
  background-color: rgb(255, 255, 255);
  color: rgb(0, 0, 0);
  border: 2px solid rgb(0, 0, 0);
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  margin-left: 10px;

  &:hover {
    background-color: rgb(0, 0, 0);
    color: rgb(255, 255, 255);
  }
`;
