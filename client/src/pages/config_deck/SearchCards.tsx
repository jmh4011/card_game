import { motion } from "framer-motion";
import React from "react";
import { styled } from "styled-components";
import filerIcon from '../../assets/icon/filter.png'
import { player_card } from "../../utils/inter";
import Card from "../../components/Card";

interface SearchCardsPorps {
  cards: player_card[]
  setShowCard: (data:any) => void
  setDeckCards: (data:any) => void
  search: string;
  setSearch: (data:string) => void;
  sortingFn: (a:any,b:any) => number
  

}

const SearchCards:React.FC<SearchCardsPorps> = ({cards,setShowCard,setDeckCards,search,setSearch, sortingFn}) => {
  
  const handlePlayerCardRightClick = (e: React.MouseEvent, value: player_card) => {
    e.preventDefault();
    setDeckCards((prev:any) => [...prev, value]);   
  };

  return <Config>
  <Container>
    <Search defaultValue={search} onChange={(e) => {setSearch(e.target.value)}}/>
    <Filter src={filerIcon} onClick={() => {setShowCard(null)}}/>
  </Container>
  <CardList>
    {Array(20).fill(cards).flat().sort(sortingFn).map((value,idx) => {
      return <CardStyle 
      key={idx}
      onClick={() => setShowCard(value)} 
      onContextMenu={(e) => handlePlayerCardRightClick(e,value)}
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}>
        <Card card={value} scale={.1} key={value.card_id}/>
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
`

const Search = styled.input`
  flex: 1;
  border: 1px solid rgb(0,0,0);
  border-radius: 10px;
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
  height: 80%;
  max-height: 80%;
  overflow-y: auto;
  gap: 10px;
  

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