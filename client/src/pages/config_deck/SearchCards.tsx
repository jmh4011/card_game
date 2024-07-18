import { motion } from "framer-motion";
import React from "react";
import { styled } from "styled-components";
import filerIcon from '../../assets/icon/filter.png'
import Card from "../../components/Card";
import { useRecoilState, useRecoilValue, useSetRecoilState } from "recoil";
import { deckCardsState, searchSettingsState, showCardState, tempDeckCardsState } from "../../atoms/modalConfigDeck";
import { cardsStats, playerCardsStats } from "../../atoms/global";
import { CardCount } from "../../utils/types";


const SearchCards:React.FC = () => {
  const cards = useRecoilValue(cardsStats)
  const playerCards = useRecoilValue(playerCardsStats);
  const [searchSettings, setSearchSettings] = useRecoilState(searchSettingsState);
  const setShowCard = useSetRecoilState(showCardState);
  const setDeckCards = useSetRecoilState(tempDeckCardsState)

  const filteredCards =  Object.keys(playerCards).map(key => Number(key)).filter(card_id => {
    let card = cards[card_id]
    let result = (searchSettings.search === '');
    if (searchSettings.search !== '') {
      if (searchSettings.searchName) result = result || card.card_name.toLowerCase().includes(searchSettings.search.toLowerCase());
      if (searchSettings.searchClass) result = result || card.card_class.toLowerCase().includes(searchSettings.search.toLowerCase());
      if (searchSettings.searchDescription) result = result || card.description.toLowerCase().includes(searchSettings.search.toLowerCase());
    }
    return result;
  });

  const sortingFn = (a: any, b: any) => {
    const orderFactor = searchSettings.order === 'Ascending' ? 1 : -1;
    if (searchSettings.stand === 'id') return (a.card_id - b.card_id) * orderFactor;
    if (searchSettings.stand === 'name') return a.card_name.localeCompare(b.card_name) * orderFactor;
    if (searchSettings.stand === 'cost') return (a.cost - b.cost) * orderFactor;
    if (searchSettings.stand === 'attack') return (a.attack - b.attack) * orderFactor;
    if (searchSettings.stand === 'health') return (a.health - b.health) * orderFactor;
    return 0;
  };

  const setSearch = (search:string) => {
    setSearchSettings(prev => ({...prev, search}))
  };



  const handlePlayerCardRightClick = (e: React.MouseEvent, value: number) => {
    e.preventDefault();
    setDeckCards((prev: CardCount) => {
      const newState = { ...prev };
      if (newState[value] !== undefined) {
          newState[value] += 1;
      } else {
          newState[value] = 1;
      }
      return newState;
    });   
  };

  return <Config>
  <Container>
    <Search defaultValue={searchSettings.search} onChange={(e) => {setSearch(e.target.value)}}/>
    <Filter src={filerIcon} onClick={() => {setShowCard(null)}}/>
  </Container>
  <CardList>
    {filteredCards.sort(sortingFn).map((value,idx) => {
      return <CardStyle 
      key={idx}
      onClick={() => setShowCard(value)} 
      onContextMenu={(e) => handlePlayerCardRightClick(e,value)}
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}>
        <Card card_id={value} scale={.1} key={value}/>
      </CardStyle>
    })}
  </CardList>
</Config>
}
export default SearchCards

const Config = styled.div`
  border: 1px solid rgb(255,0,255);
  float: left;
  width: 27%; 
  margin-left: 3%;
  margin-right: 3%;
  height: 80%;
  margin-top: 5%;
  }
`

const Container = styled.div`
  display: flex;
  align-items: center;
  margin-top: 3%;
  width: 100%;
  height: 4%;
`

const Search = styled.input`
  flex: 1;
  border: 1px solid rgb(0,0,0);
  border-radius: 5px;
  width: 80%;
  height: 100%;
  font-size: 100%;
`

const Filter = styled.img`
  margin-left: 2%;
  width: 5%;
  border: 1px solid rgb(0,0,0);
`

const CardStyle = styled(motion.div)`
  display: inline-block;
`

const CardList = styled.div`
  border: 1px solid rgb(1,255,1);
  width: 100%;
  height: 90%;
  max-height: 90%;
  overflow-y: auto;
  gap: 10px;
  margin-top:2%;
  

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

`