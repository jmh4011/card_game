import React, { useEffect, useState } from "react";
import { useSetRecoilState } from "recoil";
import { loadingState } from "../../atoms/global";
import styled from "styled-components";
import useHttpDeck from "../../api/decks";
import CardInfo from "../../components/decks/CardInfo";
import ShowDeck from "../../components/decks/ShowDeck";
import SearchCards from "../../components/decks/SearchCards";
import { OutModal } from "../../utils/styles";
import { useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar";
import { DeckCards } from "../../types/routers";
import { Deck } from "../../types/models";

interface ConfigDeckProps {
  deck: Deck;
  deckCards: DeckCards;
  setDeck: (data: any) => void;
  setDeckCards: (data: any) => void;
}

const ConfigDeckPage: React.FC<ConfigDeckProps> = ({
  deck,
  deckCards,
  setDeck,
  setDeckCards,
}) => {
  const { updateDeck } = useHttpDeck();
  const navigate = useNavigate();
  const setLoading = useSetRecoilState(loadingState);
  const [showExitCheck, setShowExitCheck] = useState<boolean>(false);
  const [showCard, setShowCard] = useState<number | null>(null);
  const [tempDeck, setTempDeck] = useState(deck);
  const [tempDeckCards, setTempDeckCards] = useState(deckCards);

  useEffect(() => {
    setTempDeck(deck);
    setTempDeckCards(deckCards);
  }, [deck, deckCards]);

  const handlePublic = () => {
    setTempDeck((pre: any) => ({ ...pre, is_public: !tempDeck.is_public }));
  };

  const handleSave = () => {
    updateDeck(
      deck.deck_id,
      {
        deck_name: tempDeck.deck_name,
        image_path: tempDeck.image_path,
        is_public: tempDeck.is_public,
        deck_cards: tempDeckCards,
      },
      (data) => {
        setDeck(data.deck);
        setDeckCards(data.deck_cards);
      }
    );
  };

  const handleExit = () => {
    if (
      JSON.stringify(tempDeckCards) === JSON.stringify(deckCards) &&
      JSON.stringify(tempDeck) === JSON.stringify(deck)
    ) {
      navigate("/deck");
    } else {
      setShowExitCheck(true);
    }
  };

  const handleUserCardRightClick = (e: React.MouseEvent, value: number) => {
    e.preventDefault();
    setTempDeckCards((prev: DeckCards) => {
      const newState = { ...prev };
      if (newState[value] !== undefined) {
        newState[value] += 1;
      } else {
        newState[value] = 1;
      }
      return newState;
    });
  };

  const handleDeckCardRightClick = (e: React.MouseEvent, value: number) => {
    e.preventDefault();
    setTempDeckCards((prev: any) => {
      const newState = { ...prev };
      if (newState[value] !== undefined) {
        newState[value] -= 1;
        if (newState[value] === 0) {
          delete newState[value];
        }
      }
      return newState;
    });
  };

  return (
    <ConfigDeckContainer>
      <Navbar name="config deck" to={handleExit}>
        <SaveButton onClick={handleSave}>save</SaveButton>
        <PublicButton onClick={handlePublic}>
          {tempDeck.is_public ? "public" : "not public"}
        </PublicButton>
      </Navbar>

      {showExitCheck && (
        <ModalExitCheck>
          <OutModal />
          <div className="in">
            <button className="cancel" onClick={() => setShowExitCheck(false)}>
              cancel
            </button>
            <button
              className="exit"
              onClick={() => {
                setShowExitCheck(false);
                navigate("/deck");
              }}
            >
              exit
            </button>
          </div>
        </ModalExitCheck>
      )}

      <InfoSection>
        {showCard && (
          <CardInfo card_id={showCard} deckCount={tempDeckCards[showCard]} />
        )}
      </InfoSection>

      <ShowDeckContainer>
        <ShowDeck
          deck={tempDeck}
          setDeck={setTempDeck}
          deckCards={tempDeckCards}
          readOnly={false}
          onCardClick={setShowCard}
          onCardContextMenu={handleDeckCardRightClick}
        />
      </ShowDeckContainer>

      <SearchCardsContainer>
        <SearchCards
          onCardClick={setShowCard}
          onCardContextMenu={handleUserCardRightClick}
        />
      </SearchCardsContainer>
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
  margin-top: 1%;
  float: left;
  border: 1px solid rgb(0, 100, 255);
  height: 90%;
  width: 20%;
`;

const PublicButton = styled.button`
  font-size: 16px;
  height: 100%;
  border-radius: 10px;
  &:hover {
    background-color: rgb(0, 0, 0);
    color: rgb(255, 255, 255);
  }
`;

const SaveButton = styled.button`
  height: 100%;
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
    width: 30%;
    height: 30%;
    background-color: rgb(255, 255, 255);
    transform: translate(-50%, -50%);
    z-index: 101;
    & .cancel {
      position: fixed;
      width: 30%;
      height: 10%;
    }
    & .exit {
      position: fixed;
      left: 50%;
      width: 30%;
      height: 10%;
    }
  }
`;

const ShowDeckContainer = styled.div`
  float: left;
  border: 1px solid black;
  width: 35%;
  height: 90%;
  margin-top: 1%;
  margin-left: 3%;
`;

const SearchCardsContainer = styled.div`
  border: 1px solid rgb(255, 0, 255);
  float: left;
  width: 35%;
  margin-left: 3%;
  height: 90%;
  margin-top: 1%;
`;
