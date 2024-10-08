import React, { useEffect, useState } from "react";
import { useSetRecoilState } from "recoil";
import { loadingState } from "../../atoms/global";
import styled from "styled-components";
import CardInfo from "../../components/decks/CardInfo";
import ShowDeck from "../../components/decks/ShowDeck";
import SearchCards from "../../components/decks/SearchCards";
import { OutModal } from "../../utils/styles";
import { useNavigate } from "react-router-dom";
import ResponsiveText from "../../components/ResponsiveText";
import Navbar from "../../components/Navbar";
import { DeckCards } from "../../types/routers";
import { Deck } from "../../types/models";

interface ReadOnlyDeckProps {
  deck: Deck;
  deckCards: DeckCards;
}

const ReadOnlyDeckPage: React.FC<ReadOnlyDeckProps> = ({ deck, deckCards }) => {
  const navigate = useNavigate();
  const setLoading = useSetRecoilState(loadingState);
  const [showExitCheck, setShowExitCheck] = useState<boolean>(false);
  const [showCard, setShowCard] = useState<number | null>(null);

  const handleExit = () => {
    navigate(-1);
  };

  const handleCardRightClick = (e: React.MouseEvent, value: number) => {
    e.preventDefault();
    setShowCard(value);
  };

  return (
    <ReadOnlyDeckContainer>
      <Navbar to={-1} name="deck">
        <ReadOnly>read only</ReadOnly>
      </Navbar>

      {showExitCheck && (
        <ModalExitCheck>
          <OutModal />
          <div className="in">
            <button onClick={() => setShowExitCheck(false)}>취소</button>
            <button
              onClick={() => {
                setShowExitCheck(false);
                navigate("/deck");
              }}
            >
              나가기
            </button>
          </div>
        </ModalExitCheck>
      )}

      <InfoSection>
        {showCard && (
          <CardInfo card_id={showCard} deckCount={deckCards[showCard]} />
        )}
      </InfoSection>

      <ShowDeckContainer>
        <ShowDeck
          deck={deck}
          deckCards={deckCards}
          readOnly={false}
          onCardClick={setShowCard}
          onCardContextMenu={handleCardRightClick}
        />
      </ShowDeckContainer>

      <SearchCardsContainer>
        <SearchCards
          onCardClick={setShowCard}
          onCardContextMenu={handleCardRightClick}
        />
      </SearchCardsContainer>
    </ReadOnlyDeckContainer>
  );
};

export default ReadOnlyDeckPage;

const ReadOnlyDeckContainer = styled.div`
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

const ReadOnly = styled.button`
  position: fixed;
  top: 0;
  right: 9%;
  width: 80px;
  height: 40px;
  font-size: 16px;
  border-radius: 10px;
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

const ShowDeckContainer = styled.div`
  float: left;
  border: 1px solid black;
  width: 35%;
  height: 80%;
  margin-top: 5%;
  margin-left: 3%;
`;

const SearchCardsContainer = styled.div`
  border: 1px solid rgb(255, 0, 255);
  float: left;
  width: 27%;
  margin-left: 3%;
  margin-right: 3%;
  height: 80%;
  margin-top: 5%;
`;
