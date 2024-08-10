import React, { useState } from "react";
import { useRecoilState, useRecoilValue, useSetRecoilState } from "recoil";
import {loadingState, showPageState} from "../../atoms/global";
import styled from "styled-components";
import useHttpDeck from "../../api/decks";
import CardInfo from "./components/CardInfo";
import SearchSetting from "./components/SearchSetting";
import ShowDeck from "./components/ShowDeck";
import SearchCards from "./components/SearchCards";
import { deckCardsState, deckState, showCardState, tempDeckCardsState, tempDeckState } from "../../atoms/modalConfigDeck";
import { OutModal } from "../../utils/styles";

const ConfigDeckPage: React.FC = () => {
  const {updateDeck} = useHttpDeck()
  const setShowPage = useSetRecoilState(showPageState);
  const setLoading = useSetRecoilState(loadingState);
  const [showExitCheck, setShowExitCheck] = useState<boolean>(false);
  const showCard = useRecoilValue(showCardState)
  const [tempDeck, setTempDeck] = useRecoilState(tempDeckState)
  const [deck, setDeck] = useRecoilState(deckState)
  const [tempDeckCards, setTempDeckCards] = useRecoilState(tempDeckCardsState)
  const [deckCards, setDeckCards] = useRecoilState(deckCardsState)
  
  const handleSave = () => {
    updateDeck(deck.deck_id, {
      deck_name: tempDeck.deck_name,
      image_path: tempDeck.image_path,
      deck_cards: tempDeckCards
    },
    (data) => {
      setDeck(data.deck);
      setDeckCards(data.deck_cards)
    });
  };

  const handleExit = () => {
    if (JSON.stringify(tempDeckCards) === JSON.stringify(deckCards) && JSON.stringify(tempDeck) ===JSON.stringify(deck)) {
      setShowPage("selectDeck");
    } else {
      setShowExitCheck(true);
    }
  };

  return (
    <ConfigDeckContainer>
      <SaveButton onClick={handleSave}>저장</SaveButton>
      <ExitButton onClick={handleExit}>나가기</ExitButton>

      {showExitCheck && (
        <ModalExitCheck>
          <OutModal />
          <div className="in">
            <button onClick={() => setShowExitCheck(false)}>취소</button>
            <button onClick={() => {setShowExitCheck(false);setShowPage("selectDeck");}}>나가기</button>
          </div>
        </ModalExitCheck>
      )}

      <InfoSection>
        {showCard ? 
          <CardInfo card_id={showCard} />:
          <SearchSetting/>
        }
      </InfoSection>

      <ShowDeck/>

      <SearchCards/>
    </ConfigDeckContainer>
  );
};

export default ConfigDeckPage;

const ConfigDeckContainer = styled.div`
  width: 100%;
  height: 100%;
`;

const InfoSection = styled.div`
  margin-left: 3%;
  margin-top: 5%;
  float: left;
  border: 1px solid rgb(0, 100, 255);
  height: 80%;
  width: 25%;
`;

const SaveButton = styled.button`
  position: fixed;
  top: 0;
  right: 9%;
  width: 80px;
  height: 40px;
  font-size: 16px;
  border-radius: 10px;
  &:hover {
    background-color: rgb(0, 0, 0);
    color: rgb(255, 255, 255);
  }
`;

const ExitButton = styled.button`
  position: fixed;
  top: 0;
  right: 0;
  width: 100px;
  height: 40px;
  font-size: 16px;
  border-radius: 10px;
  &:hover {
    background-color: rgb(0, 0, 0);
    color: rgb(255, 255, 255);
  }
`;

const ModalExitCheck = styled.div`
  & .in {
    position: fixed;
    top: 50%;
    left: 50%;
    width: 10%;
    height: 10%;
    background-color: rgb(255, 255, 255);
    transform: translate(-50%, -50%);
    z-index: 101;
  }
`;
