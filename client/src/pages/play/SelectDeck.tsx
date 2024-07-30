import React, { useState } from "react";
import { useRecoilState, useSetRecoilState } from "recoil";
import useHttpDeck from "../../api/decks";
import { decksState, showPageState} from "../../atoms/global";

import styled from "styled-components";
import { Deck } from "../../utils/types";
import { deckCardsState, deckState,  tempDeckCardsState, tempDeckState } from "../../atoms/modalConfigDeck";

const ModalSelectDeck: React.FC = () => {
  const {createDeck, getDeckCards} = useHttpDeck()
  const [decks, setDecks] = useRecoilState(decksState);
  const [scale, setScale] = useState(0.4);
  const setShowPage = useSetRecoilState(showPageState);

  const setShowDeck = useSetRecoilState(deckState);
  const setDeckCards = useSetRecoilState(deckCardsState);

  const setTempShowDeck = useSetRecoilState(tempDeckState);
  const setTempDeckCards = useSetRecoilState(tempDeckCardsState);

  const useHandleExit = () => {
    setShowPage("main")
  }



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
        <DeckContainer key={idx} scale={scale} onClick={() => HandleDeckClick(value)}>
          <DeckImg src={`/static/images/character/${value.image}`} scale={scale} />
          <DeckName scale={scale}>{value.deck_name}</DeckName>
        </DeckContainer>
      ))}
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

const DeckContainer = styled.div<{ scale: number }>`
  margin-left: 10px;
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
  border: 1px solid rgb(0,0,0);
`;


