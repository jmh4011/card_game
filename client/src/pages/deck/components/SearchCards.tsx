import React, { useState } from "react";
import { styled } from "styled-components";
import { IoSettingsOutline } from "react-icons/io5";
import ShowCard, { CardDescription } from "../../../components/ShowCard";
import { useRecoilValue } from "recoil";
import { cardsStats, userCardsStats } from "../../../atoms/global";
import SearchSetting from "./SearchSetting";

interface SearchCardsPorps {
  onCardClick: (value: number) => void;
  onCardContextMenu: (e: React.MouseEvent, value: number) => void;
}

export interface SearchSettings {
  search: string;
  order: "Ascending" | "Descending";
  stand: string;
  searchName: boolean;
  searchClass: boolean;
  searchDescription: boolean;
}

const SearchCards: React.FC<SearchCardsPorps> = ({
  onCardClick,
  onCardContextMenu,
}) => {
  const cards = useRecoilValue(cardsStats);
  const userCards = useRecoilValue(userCardsStats);
  const [searchSettings, setSearchSettings] = useState<SearchSettings>({
    search: "",
    order: "Ascending",
    stand: "id",
    searchName: true,
    searchClass: false,
    searchDescription: false,
  });
  const [showSetting, setShowSetting] = useState(false);

  const filteredCards = Object.keys(userCards)
    .map((key) => Number(key))
    .filter((card_id) => {
      let card = cards[card_id];
      let result = searchSettings.search === "";
      if (searchSettings.search !== "") {
        if (searchSettings.searchName)
          result =
            result ||
            card.card_name
              .toLowerCase()
              .includes(searchSettings.search.toLowerCase());
        if (searchSettings.searchClass)
          result =
            result ||
            card.card_class
              .toLowerCase()
              .includes(searchSettings.search.toLowerCase());
        if (searchSettings.searchDescription)
          result =
            result ||
            CardDescription(card)
              .toLowerCase()
              .includes(searchSettings.search.toLowerCase());
      }
      return result;
    });

  const sortingFn = (a: any, b: any) => {
    const orderFactor = searchSettings.order === "Ascending" ? 1 : -1;
    if (searchSettings.stand === "id")
      return (a.card_id - b.card_id) * orderFactor;
    if (searchSettings.stand === "name")
      return a.card_name.localeCompare(b.card_name) * orderFactor;
    if (searchSettings.stand === "cost") return (a.cost - b.cost) * orderFactor;
    if (searchSettings.stand === "attack")
      return (a.attack - b.attack) * orderFactor;
    if (searchSettings.stand === "health")
      return (a.health - b.health) * orderFactor;
    return 0;
  };

  const setSearch = (search: string) => {
    setSearchSettings((prev) => ({ ...prev, search }));
  };

  return (
    <Config>
      <Container>
        <Search
          defaultValue={searchSettings.search}
          onChange={(e) => {
            setSearch(e.target.value);
          }}
        />
        <Filter
          onClick={() => {
            setShowSetting(!showSetting);
          }}
        />
      </Container>
      {showSetting && (
        <div>
          <SearchSetting
            searchSettings={searchSettings}
            setSearchSettings={setSearchSettings}
          />
          <button onClick={() => setShowSetting(false)}>닫기</button>
        </div>
      )}
      <CardList>
        {filteredCards.sort(sortingFn).map((value, idx) => {
          return (
            <CardStyle
              key={idx}
              onClick={() => onCardClick(value)}
              onContextMenu={(e) => onCardContextMenu(e, value)}
            >
              <ShowCard card={cards[value]} key={value} />
            </CardStyle>
          );
        })}
      </CardList>
    </Config>
  );
};
export default SearchCards;

const Config = styled.div`
  width: 100%;
  height: 100%;
`;

const Container = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  height: 4%;
`;

const Search = styled.input`
  flex: 1;
  border: 1px solid rgb(0, 0, 0);
  border-radius: 5px;
  width: 80%;
  height: 100%;
  font-size: 100%;
`;

const Filter = styled(IoSettingsOutline)`
  margin-left: 2%;
  width: 10%;
  height: 100%;
  border: 1px solid rgb(0, 0, 0);
`;

const CardStyle = styled.div`
  display: inline-block;
  width: 25%;
`;

const CardList = styled.div`
  border: 1px solid rgb(1, 255, 1);
  width: 100%;
  height: 90%;
  max-height: 90%;
  overflow-y: auto;
  gap: 10px;
  margin-top: 2%;

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
