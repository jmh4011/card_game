import React, {  } from "react";
import styled from "styled-components";

const PlayTestPage: React.FC = () => {

  const handleDrop = (index: number, cardIndex: number) => {

  };


  return (
    <Contener>
      <Enemy>{/* <PlayerField handleCard={handleCard}/> */}</Enemy>
      <CardInfoContener>
      </CardInfoContener>
      <My>
      </My>
    </Contener>
  );
};

export default PlayTestPage;

const Contener = styled.div`
  width: 100%;
  height: 100%;
  flex-direction: column;
  display: flex;
  overflow: hidden;
`;

const Enemy = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 50%;
  border: 3px solid rgb(100, 0, 0);
  transform: scale(1, -1);
`;
const Center = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 30%;
  border: 3px solid rgb(0, 0, 0);
`;

const My = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 50%;
  border: 3px solid rgb(0, 0, 100);
`;

const CardInfoContener = styled.div`
  position: fixed;
  top: 50%;
  transform: translate(0, -50%);
  z-index: 1;
  width: 30vh;
  height: 40vh;
  border: 1px solid rgb(100, 0, 100);
`;
