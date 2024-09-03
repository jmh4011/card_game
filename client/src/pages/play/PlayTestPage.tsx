import React, { useEffect, useRef, useState } from "react";
import { useRecoilState, useRecoilValue } from "recoil";
import { cardsStats, wsTokenState } from "../../atoms/global";
import WebSocketClient from "../../api/websocket";
import PlayHomePage from "./PlayHomePage";
import useHttpGame from "../../api/game";
import { Card as CardType } from "../../utils/types";
import styled from "styled-components";
import Card from "../../components/Card";
import CardInfo from "../../components/CardInfo";

const PlayTestPage: React.FC = () => {
  const cards = useRecoilValue(cardsStats);

  const [hands, setHands] = useState<number[]>([1, 2, 3, 3]);
  const [fields, setFields] = useState<Record<number, CardType>>({});
  const [graves, setGraves] = useState<CardType[]>([]);
  const [decks, setDecks] = useState<number>(40);

  return (
    <Contener>


      <Enemy></Enemy>
      <CardInfoContener>
        <CardInfo card_id={1} deckCount={1}/>
      </CardInfoContener>
      <My>
        <MyPlayer>나</MyPlayer>
        <MyFields>
          <MyFieldCard></MyFieldCard>
          <MyFieldCard></MyFieldCard>
          <MyFieldCard></MyFieldCard>
          <MyFieldCard></MyFieldCard>
          <MyFieldCard></MyFieldCard>
        </MyFields>
        <MyHands>
          {hands.map((val, idx) => {
            return (
              <MyHandCard key={idx} index={idx} total={hands.length}>
                <Card card_id={val} />
              </MyHandCard>
            );
          })}
        </MyHands>
        <MyGraves>묘오지</MyGraves>
        <MyDeck>데엑</MyDeck>
      </My>
    </Contener>
  );
};

export default PlayTestPage;

const Contener = styled.div`
  width: 100%;
  height: 100%;
  flex-direction: column;
  overflow: hidden;
`;

const Enemy = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 49%;
  border: 3px solid rgb(100, 0, 0);
`;
const My = styled.div`
  box-sizing: border-box;
  width: 100%;
  height: 49%;
  border: 3px solid rgb(0, 0, 100);
  position: relative;
`;

const MyDeck = styled.div`
  position: absolute;
  display: flex;
  right: 0;
  bottom: 0;
  width: 15vh;
  height: 20vh;
  align-items: center;
  justify-content: center;
  border: 1px solid rgb(0, 0, 0);
`;

const MyGraves = styled.div`
  position: absolute;
  display: flex;
  right: 0;
  top: 0;
  width: 15vh;
  height: 20vh;
  align-items: center;
  justify-content: center;
  border: 1px solid rgb(0, 0, 0);
`;


const MyHands = styled.div`
  position: absolute;
  display: flex;
  left: 50%;
  bottom: -8vh;
  transform: translate(-50%);
  justify-content: flex-start;  /* 왼쪽 정렬 */
  border: 1px solid rgb(0, 0, 0);
  overflow-x: auto;  /* 스크롤 허용 */
  overflow-y: hidden;
`;

const MyHandCard = styled.div<{ index: number, total: number }>`
  position: relative;
  display: flex;
  height: 20vh;
  aspect-ratio: 3 / 4;
  box-sizing: border-box;
  flex-shrink: 0;
  

  /* 겹치기 설정 */
  &:not(:first-child) {
    margin-left: ${({ total }) => (total > 8 ? '-8vw' : '-4vw')};
  }
`

const MyPlayer = styled.div`
  position: absolute;
  display: flex;
  left: 0;
  bottom: 0;
  width: 15vw;
  height: 15vh;
  align-items: center;
  justify-content: center;
  border: 1px solid rgb(0, 0, 0);
`;
const MyFields = styled.div`
  position: absolute;
  display: flex;
  left: 50%;
  top: 0;
  transform: translate(-50%);
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
  border: 1px solid rgb(0, 0, 0);
  gap: 10px;
`;

const MyFieldCard = styled.div`
  display: flex;
  width: 10vw;
  aspect-ratio: 3 / 4; /* 3:4 비율 고정 */
  border: 1px solid rgb(100, 0, 0);
  box-sizing: border-box;
  flex-shrink: 1; /* 부모 요소가 줄어들 때 크기 줄임 */
`;


const CardInfoContener = styled.div`
  position: fixed;
  top: 50%;
  transform: translate(0, -50%);
  z-index: 1;
  height: 70vh;
  aspect-ratio: 3 / 4; /* 3:4 비율 고정 */


`