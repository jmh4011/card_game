import React from "react";
import { useNavigate } from "react-router-dom";
import ShowDecks from "../../components/ShowDecks";
import { Deck } from "../../utils/types";
import useHttpUser from "../../api/users";
import { useRecoilValue } from "recoil";
import { userStats } from "../../atoms/global";
import Navbar from "../../components/Navbar";

const PlayDeckSelectPage = () => {
  const navigate = useNavigate();
  const { updateUserDeckSelection } = useHttpUser();
  const user = useRecoilValue(userStats);

  const handleDeckClick = (deck: Deck) => {
    updateUserDeckSelection(
      {
        deck_id: deck.deck_id,
        mod_id: user.current_mod_id,
      },
      (data) => {}
    );
  };

  return (
    <div>
      <Navbar to={"/play/home"} name="select play deck"></Navbar>
      <ShowDecks
        handleDeckClick={handleDeckClick}
        createButton
      />
    </div>
  );
};

export default PlayDeckSelectPage;
