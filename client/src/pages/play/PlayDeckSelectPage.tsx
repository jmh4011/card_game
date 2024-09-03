import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ShowDecks from "../../components/ShowDecks";
import { Deck } from "../../utils/types";
import useHttpUser from "../../api/users";
import { useRecoilValue } from "recoil";
import { userStats } from "../../atoms/global";
import Navbar from "../../components/Navbar";
import styled from "styled-components";
import useHttpDeck from "../../api/decks";
import { characterImage } from "../../api/static";

const PlayDeckSelectPage = () => {
  const navigate = useNavigate();
  const { updateUserDeckSelection } = useHttpUser();
  const user = useRecoilValue(userStats);
  const { getDecks, createDeck } = useHttpDeck();
  const [decks, setDecks] = useState<Deck[]>([]);

  const handleDeckClick = (deck: Deck) => {
    updateUserDeckSelection(
      {
        deck_id: deck.deck_id,
        mod_id: user.current_mod_id,
      },
      (data) => {}
    );

    navigate("/play/home")
  };


  useEffect(() => {
    getDecks((data) => {
      setDecks(data);
    });
  }, []);

  return (
    <Modal>
      <Navbar name="play deck select" to={"/play/home"} />
      <Container>
        {decks.map((value, idx) => (
          <DeckContainer key={idx} onClick={() => handleDeckClick(value)}>
            <DeckImg src={characterImage(value.image_path)} />
            <DeckName>{value.deck_name}</DeckName>
          </DeckContainer>
        ))}
      </Container>
    </Modal>
  );
};

export default PlayDeckSelectPage;

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
