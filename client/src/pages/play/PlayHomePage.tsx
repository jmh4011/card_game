import React, { useEffect, useState } from "react";
import styled from "styled-components";
import useHttpUser from "../../api/users";
import { Deck, DeckSelection, GameMod } from "../../utils/types";
import useHttpDeck from "../../api/decks";
import { useRecoilState } from "recoil";
import { userStats } from "../../atoms/global";
import useHttpGame from "../../api/game";
import { characterImage } from "../../api/static";

const PlayHomePage: React.FC = () => {
  const { getUserDeckSelection } = useHttpUser();
  const { getDecks } = useHttpDeck();
  const { getMod } = useHttpGame();
  const [deck, setDeck] = useState<Deck>();
  const [mod, setMod] = useState<GameMod>();
  const [user, setUser] = useRecoilState(userStats);

  useEffect(() => {
    getUserDeckSelection(user.current_mod_id, (data) => {
      setDeck(data);
    });
    getMod(user.current_mod_id, (data) => {
      setMod(data);
    });
  }, [user]);

  const handleDeckClick = () => {};

  return (
    <div>
      <DeckContainer onClick={() => handleDeckClick()}>
        {deck ? (
          <>
            <DeckImg src={characterImage(deck.image_path)} />
            <DeckName>{deck.deck_name}</DeckName>
          </>
        ) : (
          <div>deck select</div>
        )}
      </DeckContainer>

      <ModContainer onClick={() => handleDeckClick()}>
        {mod ? (
          <>
            <ModImg src={characterImage(mod.image_path)} />
            <ModName>{mod.mod_name}</ModName>
          </>
        ) : (
          <div>mod select</div>
        )}
      </ModContainer>

      <div>플레이 버튼</div>
    </div>
  );
};

export default PlayHomePage;

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

const ModContainer = styled.div`
  margin-left: 10px;
  display: inline-block;
  width: 15%;
  height: 40%;
  border: 1px solid rgb(0, 0, 0);
  text-align: center;
  cursor: pointer;
`;

const ModImg = styled.img`
  height: 100%;
  width: 100%;
`;

const ModName = styled.div`
  font-size: 30px;
  border: 1px solid rgb(0, 0, 0);
`;
