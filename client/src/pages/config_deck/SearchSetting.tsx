import React from "react";
import { useRecoilState } from "recoil";
import styled from "styled-components";
import { searchSettingsState } from "../../atoms/modalConfigDeck";



const SearchSetting: React.FC = () => {
  
  const [searchSettings, setSearchSettings] = useRecoilState(searchSettingsState);
  const setOrder = (order:'Ascending' | 'Descending') => setSearchSettings(prev => ({ ...prev, order }))
  const setStand = (stand:string) => setSearchSettings(prev => ({ ...prev, stand }))
  const setSearchName = (searchName:boolean) => setSearchSettings(prev => ({ ...prev, searchName }))
  const setSearchClass = (searchClass:boolean) => setSearchSettings(prev => ({ ...prev, searchClass }))
  const setSearchDescription = (searchDescription:boolean) => setSearchSettings(prev => ({ ...prev, searchDescription }))
          


  return (
    <FilterSetting>
      <Order>
        <label>
          <input
            type="radio"
            value="Ascending"
            checked={searchSettings.order === 'Ascending'}
            onChange={() => setOrder('Ascending')}
          />
          오름차순
        </label>
        <label>
          <input
            type="radio"
            value="Descending"
            checked={searchSettings.order === 'Descending'}
            onChange={() => setOrder('Descending')}
          />
          내림차순
        </label>
      </Order>
      <Sort>
        <label htmlFor="selectBox">정렬 기준:</label>
        <select id="selectBox" defaultValue={searchSettings.stand} 
        onChange={(e) => setStand(e.target.value)}>
          <option value="id">id순</option>
          <option value="name">이름순</option>
          <option value="cost">코스트순</option>
          <option value="attack">공격력순</option>
          <option value="health">체력순</option>
        </select>
      </Sort>
      <Search>
        <label>
          <input type="checkbox" defaultChecked={searchSettings.searchName} 
          onChange={(e) => setSearchName(e.target.checked)} />
          이름
        </label>
        <label>
          <input type="checkbox" defaultChecked={searchSettings.searchClass} 
          onChange={(e) => setSearchClass(e.target.checked)} />
          종족
        </label>
        <label>
          <input type="checkbox" defaultChecked={searchSettings.searchDescription} 
          onChange={(e) => setSearchDescription(e.target.checked)} />
          효과
        </label>
      </Search>
    </FilterSetting>
  );
};

export default SearchSetting;

const FilterSetting = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
`;

const Order = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const Sort = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;

  select {
    margin-top: 5px;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
`;

const Search = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;

  label {
    display: flex;
    align-items: center;
    gap: 5px;
  }
`;
