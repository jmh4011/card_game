import React from "react";
import styled from "styled-components";

interface SearchSettingProps {
  order: 'Ascending' | 'Descending';
  setOrder: (data: 'Ascending' | 'Descending') => void;
  stand: string;
  setStand: (data: string) => void;
  searchName: boolean;
  searchClass: boolean;
  searchDescription: boolean;
  setSearchName: (data: boolean) => void;
  setSearchClass: (data: boolean) => void;
  setSearchDescription: (data: boolean) => void;
}

const SearchSetting: React.FC<SearchSettingProps> = ({
  order, setOrder,
  stand, setStand,
  searchName, setSearchName,
  searchClass, setSearchClass,
  searchDescription, setSearchDescription
}) => {
  return (
    <FilterSetting>
      <Order>
        <label>
          <input
            type="radio"
            value="Ascending"
            checked={order === 'Ascending'}
            onChange={() => setOrder('Ascending')}
          />
          오름차순
        </label>
        <label>
          <input
            type="radio"
            value="Descending"
            checked={order === 'Descending'}
            onChange={() => setOrder('Descending')}
          />
          내림차순
        </label>
      </Order>
      <Sort>
        <label htmlFor="selectBox">정렬 기준:</label>
        <select id="selectBox" defaultValue={stand} onChange={(e) => setStand(e.target.value)}>
          <option value="id">id순</option>
          <option value="name">이름순</option>
          <option value="cost">코스트순</option>
          <option value="attack">공격력순</option>
          <option value="health">체력순</option>
        </select>
      </Sort>
      <Search>
        <label>
          <input type="checkbox" defaultChecked={searchName} onChange={(e) => setSearchName(e.target.checked)} />
          이름
        </label>
        <label>
          <input type="checkbox" defaultChecked={searchClass} onChange={(e) => setSearchClass(e.target.checked)} />
          종족
        </label>
        <label>
          <input type="checkbox" defaultChecked={searchDescription} onChange={(e) => setSearchDescription(e.target.checked)} />
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
