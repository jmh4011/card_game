import React from "react";
import { Deck } from "../../utils/types";
import ShowDecks from "../../components/ShowDecks";
import { useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar";

const SelectConfigDecksPage: React.FC = () => {
  const navigate = useNavigate();
  const handleExit = () => {
    navigate("/");
  };

  const handleDeckClick = (deck: Deck) => {
    navigate(`/deck/${deck.deck_id}`);
  };

  return (
    <>
      <Navbar to="/" name="select deck"></Navbar>
      <ShowDecks
        handleDeckClick={handleDeckClick}
        createButton
      />
    </>
  );
};

export default SelectConfigDecksPage;
