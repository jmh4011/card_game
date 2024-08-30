import React, { useEffect, useState } from "react";
import styled from "styled-components";
import useHttpUser from "../../api/users";
import { Deck, DeckSelection, GameMod } from "../../utils/types";
import useHttpDeck from "../../api/decks";
import { useRecoilState } from "recoil";
import { userStats } from "../../atoms/global";
import useHttpGame from "../../api/game";
import { characterImage } from "../../api/static";
import { useNavigate } from "react-router-dom";
import ResDescription from "../../components/ResDescription";
import ScrollableDescription from "../../components/ScrollableDescription";

const PlayHomePage: React.FC = () => {
  const { getUserDeckSelection } = useHttpUser();
  const navigate = useNavigate();
  const { getDecks } = useHttpDeck();
  const { getMods } = useHttpGame();
  const [decks, setDecks] = useState<Record<number, Deck>>();
  const [mods, setMods] = useState<GameMod[]>();
  const [user, setUser] = useRecoilState(userStats);

  useEffect(() => {
    getUserDeckSelection((data) => {
      setDecks(data);
    });
    getMods((data) => {
      setMods(data);
    });
  }, [user]);

  const handleDeckClick = () => {
    navigate("/play/deck");
  };

  const handleModClick = (val: GameMod) => {
    navigate("/play/mod");
  };

  return (
    <Container>
      <ModContainer>
        {mods?.map((val, idx) => {
          return (
            <ModBox key={idx} onClick={() => handleModClick(val)}>
              <ModImg src={characterImage(val.image_path)} />
              <ModTextContainer>
                <ModName>{val.mod_name}</ModName>
                  <ModDescription>
                    <ScrollableDescription>{val.description}</ScrollableDescription>
                  </ModDescription>
              </ModTextContainer>
            </ModBox>
          );
        })}
      </ModContainer>

      <DeckContainer onClick={() => handleDeckClick()}>
        {decks && decks[user.current_mod_id] ? (
          <>
            <DeckImg
              src={characterImage(decks[user.current_mod_id].image_path)}
            />
            <DeckName>{decks[user.current_mod_id].deck_name}</DeckName>
          </>
        ) : (
          <>
            <DeckImg
              src={characterImage("3.png")}
            />
            <DeckName>deck select</DeckName>
          </>
        )}
      </DeckContainer>
      <PlayButton>play</PlayButton>
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
  margin-top: 10px;
  width: 100%;
  height: 20%;
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
  width: 20%;
  height: 20%;
  font-size: 30px;
  border: 1px solid rgb(0, 0, 0);

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

const PlayButton = styled.button`

`