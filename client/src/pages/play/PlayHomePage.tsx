import React, { useEffect, useState } from "react";
import styled from "styled-components";
import useHttpUser from "../../api/users";
import useHttpDeck from "../../api/decks";
import { useRecoilState } from "recoil";
import { userStats } from "../../atoms/global";
import useHttpGame from "../../api/game";
import { characterImage } from "../../api/static";
import { useNavigate } from "react-router-dom";
import ResDescription from "../../components/ResDescription";
import ScrollableDescription from "../../components/ScrollableDescription";
import Navbar from "../../components/Navbar";
import { Deck, GameMod } from "../../types/models";

const PlayHomePage: React.FC = () => {
  const { getUserDeckSelection } = useHttpUser();
  const navigate = useNavigate();
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

  const handleDeckClick = () => {
    navigate("/play/deck");
  };

  const handleModClick = () => {
    navigate("/play/mod");
  };

  const handlePlayClick = () => {
    navigate("/play")
  }

  return (
    <Container>
      <Navbar name="play home" to={"/"} />
      {mod ? (
        <ModBox onClick={handleModClick}>
          <ModImg src={characterImage(mod.image_path)} />
          <ModTextContainer>
            <ModName>{mod.mod_name}</ModName>
            <ModDescription>
              <ScrollableDescription>{mod.description}</ScrollableDescription>
            </ModDescription>
          </ModTextContainer>
        </ModBox>
      ) : (
        <ModBox onClick={handleModClick}></ModBox>
      )}

      <DeckContainer onClick={() => handleDeckClick()}>
        {deck ? (
          <>
            <DeckImg src={characterImage(deck.image_path)} />
            <DeckName>{deck.deck_name}</DeckName>
          </>
        ) : (
          <>
            <DeckImg src={characterImage("3.png")} />
            <DeckName>deck select</DeckName>
          </>
        )}
      </DeckContainer>
      <PlayButton onClick={handlePlayClick}>play</PlayButton>
    </Container>
  );
};

export default PlayHomePage;

const Container = styled.div`
  width: 100%;
  height: 100%;
`;

const ModContainer = styled.div`
  margin-top: 10px;
  margin-left: 10px;
  float: left;
  width: 60%;
  height: 90%;
  border: 1px solid rgb(0, 0, 100);
  max-height: 90%;
  overflow-y: auto;
  overflow-x: hidden;
  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
  }

  &::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 10px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: #555;
  }
`;

const ModBox = styled.div`

  width: 60%;
  height: 20%;
  float: left;
  margin-top: 10px;
  border: 1px solid rgb(0, 0, 0);
  display: flex;
  align-items: flex-start;
`;

const ModImg = styled.img`
  height: 100%;
  display: inline-block;
  border: 1px solid rgb(0, 0, 0);
`;

const ModTextContainer = styled.div`
  height: 100%;
  display: flex;
  flex-direction: column;
  margin-left: 10px;
  margin-right: 10px;
  flex-grow: 1;
`;

const ModName = styled.div`
  font-size: 30px;
  border: 1px solid rgb(0, 0, 0);
  display: inline;

  padding: 0 5px;
  margin: 0;
  line-height: 1;
`;

const ModDescription = styled.div`
  padding: 5px;
  border: 1px solid rgb(0, 0, 0);
  margin-top: 5px;
  height: 60%;
`;

const DeckContainer = styled.div`
  margin-left: 10px;
  float: left;
  width: 30%;
  border: 1px solid rgb(0, 0, 0);
  text-align: center;
  cursor: pointer;
`;

const DeckImg = styled.img`
  width: 100%;
`;

const DeckName = styled.div`
  font-size: 30px;
  border: 1px solid rgb(0, 0, 0);
`;

const PlayButton = styled.button``;
