import React, { useState } from "react";
import { useRecoilState, useRecoilValue, useSetRecoilState } from "recoil";
import { deckCardsState, decksState, loadingState, playerCardsStats, showDeckState, showPageState, userIdState } from "../recoli/atom";
import styled from "styled-components";
import Card from "../components/Card";
import { player_card } from "../utils/inter";
import { PutDeckUpdate } from "../api/api";
import CardInfo from "./config_deck/CardInfo";
import SearchSetting from "./config_deck/SearchSetting";
import ShowDeck from "./config_deck/ShowDeck";
import SearchCards from "./config_deck/SearchCards";

const ModalConfigDeck: React.FC = () => {
  const userId = useRecoilValue(userIdState);
  const setShowPage = useSetRecoilState(showPageState);
  const setLoading = useSetRecoilState(loadingState);
  const [showDeck,setShowDeck] = useRecoilState(showDeckState);
  const currentDeckCards = useRecoilValue(deckCardsState);
  const setDeckState = useSetRecoilState(deckCardsState);
  const [deck, setDeck] = useState(showDeck);
  const [deckCards, setDeckCards] = useState(currentDeckCards);
  const [playerCards, setPlayerCards] = useRecoilState(playerCardsStats);
  const [showCard, setShowCard] = useState<player_card | null>(null);
  const [search, setSearch] = useState<string>('');
  const [order, setOrder] = useState<'Ascending' | 'Descending'>('Ascending');
  const [stand, setStand] = useState<string>('id');
  const [searchName, setSearchName] = useState<boolean>(true);
  const [searchClass, setSearchClass] = useState<boolean>(false);
  const [searchDescription, setSearchDescription] = useState<boolean>(false);
  const [showExitCheck, setShowExitCheck] = useState<boolean>(false);

  const sortingFn = (a: any, b: any) => {
    const orderFactor = order === 'Ascending' ? 1 : -1;
    if (stand === 'id') return (a.card_id - b.card_id) * orderFactor;
    if (stand === 'name') return a.card_name.localeCompare(b.card_name) * orderFactor;
    if (stand === 'cost') return (a.cost - b.cost) * orderFactor;
    if (stand === 'attack') return (a.attack - b.attack) * orderFactor;
    if (stand === 'health') return (a.health - b.health) * orderFactor;
    return 0;
  };

  const filteredCards = playerCards.filter(card => {
    let result = (search === '');
    if (search !== '') {
      if (searchName) result = result || card.card_name.toLowerCase().includes(search.toLowerCase());
      if (searchClass) result = result || card.card_class.toLowerCase().includes(search.toLowerCase());
      if (searchDescription) result = result || card.description.toLowerCase().includes(search.toLowerCase());
    }
    return result;
  });

  const handleSave = async () => {
    PutDeckUpdate(deck.deck_id, {
      deck_name: deck.deck_name,
      image: deck.image,
      deck_cards: deckCards.map(value => value.card_id).sort((a: number, b: number) => a - b)
    }, setShowDeck, setDeckState, setLoading);
    console.log(currentDeckCards)
    console.log(deckCards)
  };

  const handleExit = () => {
    if (currentDeckCards === deckCards && showDeck === deck) {
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
          <div className="out"></div>
          <div className="in"> </div>
        </ModalExitCheck>
      )}

      <InfoSection>
        {showCard ? (
          <CardInfo card={showCard} />
        ) : (
          <SearchSetting
            order={order}
            setOrder={setOrder}
            stand={stand}
            setStand={setStand}
            searchName={searchName}
            setSearchName={setSearchName}
            searchClass={searchClass}
            setSearchClass={setSearchClass}
            searchDescription={searchDescription}
            setSearchDescription={setSearchDescription}
          />
        )}
      </InfoSection>

      <ShowDeck
        deck={deck}
        setDeck={setDeck}
        deckCards={deckCards}
        setDeckCards={setDeckCards}
        setShowCard={setShowCard}
      />

      <SearchCards
        cards={filteredCards}
        sortingFn={sortingFn}
        search={search}
        setSearch={setSearch}
        setDeckCards={setDeckCards}
        setShowCard={setShowCard}
      />
    </ConfigDeckContainer>
  );
};

export default ModalConfigDeck;

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
  right: 6%;
  width: 5%;
  height: 4%;
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
  width: 5%;
  height: 4%;
  font-size: 16px;
  border-radius: 10px;
  &:hover {
    background-color: rgb(0, 0, 0);
    color: rgb(255, 255, 255);
  }
`;

const ModalExitCheck = styled.div`
  & .out {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.2);
    z-index: 100;
  }
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
