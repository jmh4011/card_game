import React, { useState } from "react";
import { useRecoilState, useSetRecoilState } from "recoil";
import useHttpDeck from "../../api/decks";
import { decksState, showPageState} from "../../atoms/global";
import styled from "styled-components";
import { Deck } from "../../utils/types";
import { deckCardsState, deckState,  tempDeckCardsState, tempDeckState } from "../../atoms/modalConfigDeck";
import { characterImage } from "../../api/static";
import ModalSelectDeck from "../../components/ModalSelectDeck";

const SelectDeckPage: React.FC = () => {
  const {createDeck, getDeckCards} = useHttpDeck()
  const [decks, setDecks] = useRecoilState(decksState);
  const setShowPage = useSetRecoilState(showPageState);

  const setShowDeck = useSetRecoilState(deckState);
  const setDeckCards = useSetRecoilState(deckCardsState);

  const setTempShowDeck = useSetRecoilState(tempDeckState);
  const setTempDeckCards = useSetRecoilState(tempDeckCardsState);

  const handleExit = () => {
    setShowPage("home")
  }

  const handleDeckClick = (deck: Deck) => {
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

  return <ModalSelectDeck handleExit={handleExit} handleDeckClick={handleDeckClick}/>
};

export default SelectDeckPage;
