import React, { useEffect, useState } from "react";
import { Deck } from "../../utils/types";
import { useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar";
import styled from "styled-components";
import { characterImage } from "../../api/static";
import useHttpDeck from "../../api/decks";

const SelectConfigDecksPage: React.FC = () => {
  const navigate = useNavigate();
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


  const handleDeckClick = (deck: Deck) => {
    navigate(`/deck/${deck.deck_id}`);
  };

  return (
    <Modal>
      <Navbar name="select deck" to={"/home"} />
      <Container>
        {decks.map((value, idx) => (
          <DeckContainer key={idx} onClick={() => handleDeckClick(value)}>
            <DeckImg src={characterImage(value.image_path)} />
            <DeckName>{value.deck_name}</DeckName>
          </DeckContainer>
        ))}
        
          <CreateButton onClick={handleCreate}>Create Deck</CreateButton>
      </Container>
    </Modal>
  );
};

export default SelectConfigDecksPage;

const Modal = styled.div`
  width: 100%;
  height: 100%;
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
