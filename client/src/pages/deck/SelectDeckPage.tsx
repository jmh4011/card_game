import React, { useEffect, useState } from "react";
import { Deck } from "../../utils/types";
import ModalSelectDeck from "../../components/ModalSelectDeck";
import { useNavigate } from "react-router-dom";

const SelectDeckPage: React.FC = () => {
  // const {createDeck, getDeckCards} = useHttpDeck()
  // const [decks, setDecks] = useState<Deck[]>([]);
  // const setShowPage = useSetRecoilState(showPageState);

  // const setShowDeck = useSetRecoilState(deckState);
  // const setDeckCards = useSetRecoilState(deckCardsState);

  // const setTempShowDeck = useSetRecoilState(tempDeckState);
  // const setTempDeckCards = useSetRecoilState(tempDeckCardsState);


  const navigate = useNavigate();
  const handleExit = () => {
    navigate("/");
  };

  const handleDeckClick = (deck: Deck) => {
    navigate(`/deck/${deck.deck_id}`);
  };

  return (
    <ModalSelectDeck
      handleExit={handleExit}
      handleDeckClick={handleDeckClick}
    />
  );
};

export default SelectDeckPage;
