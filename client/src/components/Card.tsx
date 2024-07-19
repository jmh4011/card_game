import React from "react";
import styled from "styled-components";
import baseSprites from '../assets/base_sprites.png';
import { useRecoilValue } from "recoil";
import { cardsStats } from "../atoms/global";

interface CardProps {
  card_id: number;
}

const Card: React.FC<CardProps> = ({ card_id }) => {
  const card = useRecoilValue(cardsStats)[card_id]

  return (
    <CardContainer>
      <CardFrame>
        <Character src={`/static/images/character/${card.image}`} alt="" />
        <CharacterFrame />
        <Name>{card.card_name}</Name>
        <Cost>{card.cost}</Cost>
        <Text>{card.description}</Text>
        {card.card_type === 0 && (
          <>
            <Attack>{card.attack}</Attack>
            <Health>{card.health}</Health>
          </>
        )}
        <Type>{card.card_class}</Type>
      </CardFrame>
    </CardContainer>
  );
};

export default Card;

const CardContainer = styled.div`
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const IconLink = styled.div`
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  background-image: url(${baseSprites});
  background-repeat: no-repeat;
  background-size: contain;
  font-weight: bold;
`;

const CardFrame = styled(IconLink)`
  width: 100%;
  height: 100%;
  background-position: -10px -10px;
`;

const CharacterFrame = styled(IconLink)`
  width: 92.38%;
  height: 48.43%;
  background-position: -660px -10px;
  top: 27%;
  left: 50%;
  transform: translate(-50%, -50%);
  & > img {
    position: absolute;
    width: 99%;
    height: 99%;
    z-index: -1; /* Places the img behind the background */
  }
`;

const Character = styled.img`
  position: absolute;
  width: 88.89%;
  height: 45.78%;
  top: 27%;
  left: 50%;
  transform: translate(-50%, -50%);
`;

const Name = styled(IconLink)`
  width: 69.84%;
  height: 10.72%;
  background-position: -660px -726px;
  top: 47%;
  left: 50%;
  transform: translateX(-50%);
  color: black;
  font-size: ${({ children }) => {
    const length = (children as string).length;
    return length < 15 ? '3.6vw' : '1.8vw'; // Adjust font size based on length
  }};
`;

const Attack = styled(IconLink)`
  width: 21.9%;
  height: 19.88%;
  background-position: -1262px -10px;
  bottom: 3%;
  left: 3%;
  font-size: 6vw;
`;

const Health = styled(IconLink)`
  width: 23.49%;
  height: 19.64%;
  background-position: -10px -962px;
  bottom: 2%;
  right: 2%;
  font-size: 6vw;
`;

const Cost = styled(IconLink)`
  width: 20.48%;
  height: 15.54%;
  background-position: -1262px -195px;
  top: 2%;
  left: 2%;
  font-size: 6vw;
`;

const Text = styled(IconLink)`
  width: 92.38%;
  height: 33.01%;
  background-position: -660px -432px;
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
  font-size: ${({ children }) => {
    const length = (children as string).length;
    return length < 50 ? '3vw' : '1.8vw'; // Adjust font size based on length
  }};
`;

const Type = styled(IconLink)`
  width: 52.7%;
  height: 9.88%;
  background-position: -10px -860px;
  bottom: 5%;
  left: 50%;
  transform: translateX(-50%);
  font-size: 3vw;
`;
