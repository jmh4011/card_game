import React, { useEffect, useRef, useState } from "react";
import { useRecoilState, useRecoilValue } from "recoil";
import { cardsStats, wsTokenState } from "../../atoms/global";
import { Card as CardType } from "../../utils/types";
import styled from "styled-components";
import Card from "../../components/ShowCard";
import CardInfo from "./components/CardInfo";
import PlayerField from "./components/PlayerField";

const PlayTestPage: React.FC = () => {
  const cards = useRecoilValue(cardsStats);

  const [hands, setHands] = useState<number[]>([1, 2, 3, 3]);
  const [fields, setFields] = useState<Record<number, CardType>>({});
  const [graves, setGraves] = useState<CardType[]>([]);
  const [decks, setDecks] = useState<number>(40);
  const [showCardInfo, setShowCardInfo] = useState<number>(1)

  const handleCard = (val:number) => {
    setShowCardInfo(val)
  }

  return (
    <Contener>
      <Enemy>
        {/* <PlayerField handleCard={handleCard}/> */}
      </Enemy>
      <CardInfoContener>
        <CardInfo card_id={showCardInfo} />
      </CardInfoContener>
      <My>
        <PlayerField handleCard={handleCard}/>
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
  transform: scale(1, -1)
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
