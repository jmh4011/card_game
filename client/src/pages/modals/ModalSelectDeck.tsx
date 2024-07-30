import React, { useState } from "react";
import { useRecoilState, useSetRecoilState } from "recoil";
import useHttpDeck from "../../api/decks";
import { decksState, showPageState} from "../../atoms/global";

import styled from "styled-components";
import { Deck } from "../../utils/types";
import { deckCardsState, deckState,  tempDeckCardsState, tempDeckState } from "../../atoms/modalConfigDeck";
import { characterImage } from "../../api/static";

const ModalSelectDeck: React.FC = () => {
  const {createDeck, getDeckCards} = useHttpDeck()
  const [decks, setDecks] = useRecoilState(decksState);
  const setShowPage = useSetRecoilState(showPageState);

  const setShowDeck = useSetRecoilState(deckState);
  const setDeckCards = useSetRecoilState(deckCardsState);

  const setTempShowDeck = useSetRecoilState(tempDeckState);
  const setTempDeckCards = useSetRecoilState(tempDeckCardsState);

  const useHandleExit = () => {
    setShowPage("main")
  }


  const HandleCreate = () => {
    createDeck((data) => { setDecks((prev) => [...prev, data]);});
  };

  const HandleDeckClick = (deck: Deck) => {
    console.log(deck);
    setShowDeck(deck);
    setTempShowDeck(deck);

    getDeckCards(deck.deck_id,
      (data) => {
        setDeckCards(data);
        setTempDeckCards(data);
      }
    )
    setShowPage("configDeck");
  };

  return <Modal>
    <Menu>
      <ExitButton onClick={useHandleExit}>Eixt</ExitButton>
    </Menu>
    <Container>
      {decks.map((value, idx) => (
        <DeckContainer key={idx} onClick={() => HandleDeckClick(value)}>
          <DeckImg src={characterImage(value.image)}/>
          <DeckName>{value.deck_name}</DeckName>
        </DeckContainer>
      ))}
      <CreateButton onClick={HandleCreate}>Create Deck</CreateButton>
    </Container>
  </Modal>
};

export default ModalSelectDeck;

const Modal = styled.div`
  width: 100%;
  height: 100%;
`

const Menu = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 50px;
  border: 1px solid rgb(0, 0, 0);
`

const ExitButton = styled.button`
  position: fixed;
  top: 0;
  right: 0;
  width: 5%;
  height: 4%;
  font-size: 16px;
  border-radius: 10px;
  &:hover {
    background-color: rgb(0, 0, 0);
    color: rgb(255, 255, 255);
  }
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
  border: 1px solid rgb(0,0,0);
`;

const CreateButton = styled.button`
  width: 200px;
  height: 50px;
  background-color: rgb(255, 255, 255);
  color: rgb(0, 0, 0);
  border: 2px solid rgb(0,0,0);
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  margin-left: 10px;

  &:hover {
    background-color: rgb(0, 0, 0);
    color: rgb(255,255,255)
  }
`;
