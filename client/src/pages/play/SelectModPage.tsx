import React, { useEffect, useState } from "react";
import { useRecoilState, useRecoilValue } from "recoil";
import useHttpGame from "../../api/game";
import { GameMod } from "../../utils/types";
import { useNavigate } from "react-router-dom";
import { characterImage } from "../../api/static";
import styled from "styled-components";
import { userStats } from "../../atoms/global";
import useHttpUser from "../../api/users";

const SelectModPage: React.FC = ({}) => {
  const { getMods } = useHttpGame();
  const { updateUserStat } = useHttpUser();
  const [mods, setMods] = useState<GameMod[]>([]);
  const navigate = useNavigate();
  const user = useRecoilValue(userStats);

  useEffect(() => {
    getMods((data) => {
      setMods(data);
    });
  }, []);

  const handleExit = () => {
    navigate("/play");
  };

  const handleModClick = (value: GameMod) => {
    updateUserStat({ ...user, current_mod_id: value.mod_id });
    navigate("/play");
  };

  return (
    <Modal>
      <Menu>
        <ExitButton onClick={handleExit}>Eixt</ExitButton>
      </Menu>
      <Container>
        {mods.map((value, idx) => (
          <ModContainer key={idx} onClick={() => handleModClick(value)}>
            <ModName>{value.mod_name}</ModName>
            <ModImg src={characterImage(value.image_path)} />
            <ModDescription>{value.description}</ModDescription>
          </ModContainer>
        ))}
      </Container>
    </Modal>
  );
};

export default SelectModPage;

const Modal = styled.div`
  width: 100%;
  height: 100%;
`;

const Menu = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 50px;
  border: 1px solid rgb(0, 0, 0);
`;

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

const ModDescription = styled.div`
  border: 1px solid rgb(100, 0, 0);
`;
