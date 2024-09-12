import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useRecoilState } from "recoil";
import styled from "styled-components";
import useHttpDeck from "../../api/decks";
import useHttpGame from "../../api/game";
import { characterImage } from "../../api/static";
import useHttpUser from "../../api/users";
import { userStats } from "../../atoms/global";
import ScrollableDescription from "../../components/ScrollableDescription";
import Navbar from "../../components/Navbar";
import { GameMod } from "../../types/models";

const PlayModSelectPage: React.FC = () => {
  const navigate = useNavigate();
  const { getMods } = useHttpGame();
  const { updateUserStat } = useHttpUser();
  const [mods, setMods] = useState<GameMod[]>([]);
  const [user, setUser] = useRecoilState(userStats);

  useEffect(() => {
    getMods((data) => {
      setMods(data);
    });
  }, []);

  const handleModClick = (val: GameMod) => {
    updateUserStat({
      current_mod_id: val.mod_id,
      nickname: null,
      money: null,
    });
  };

  return (
    <Container>
      <Navbar name="mod select" to="/play/home" />
      <ModContainer>
        {mods.map((val, idx) => {
          return val.mod_id === user.current_mod_id ? (
            <ModBoxStress key={idx} onClick={() => handleModClick(val)}>
              <ModImg src={characterImage(val.image_path)} />
              <ModTextContainer>
                <ModName>{val.mod_name}</ModName>
                <ModDescription>
                  <ScrollableDescription>
                    {val.description}
                  </ScrollableDescription>
                </ModDescription>
              </ModTextContainer>
            </ModBoxStress>
          ) : (
            <ModBox key={idx} onClick={() => handleModClick(val)}>
              <ModImg src={characterImage(val.image_path)} />
              <ModTextContainer>
                <ModName>{val.mod_name}</ModName>
                <ModDescription>
                  <ScrollableDescription>
                    {val.description}
                  </ScrollableDescription>
                </ModDescription>
              </ModTextContainer>
            </ModBox>
          );
        })}
      </ModContainer>
    </Container>
  );
};

export default PlayModSelectPage;

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
  width: 95%;
  height: 20%;
  border: 1px solid rgb(0, 0, 0);
  display: flex;
  align-items: flex-start;
`;

const ModBoxStress = styled.div`
  margin-top: 10px;
  width: 95%;
  height: 20%;
  border: 5px solid rgb(150, 0, 0);
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
