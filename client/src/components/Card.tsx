import React from "react";
import styled from "styled-components";
import attackImg from '../assets/card-base/attack.png';
import characterFrameImg from '../assets/card-base/character-frame.png';
import classImg from '../assets/card-base/class.png';
import costImg from '../assets/card-base/cost.png';
import descriptionImg from '../assets/card-base/description.png';
import frameImg from '../assets/card-base/frame.png';
import healthImg from '../assets/card-base/health.png';
import nameImg from '../assets/card-base/name.png';
import { useRecoilValue } from "recoil";
import { cardsStats } from "../atoms/global";
import { characterImage } from "../api/static";
import ResponsiveText from "./ResponsiveText";

interface CardProps {
  card_id: number;
}

const Card: React.FC<CardProps> = ({ card_id }) => {
  const card = useRecoilValue(cardsStats)[card_id];

  return (
    <CardContainer>
      <CardFrame>
        <CharacterFrame />
        <Character src={characterImage(card.image)} />
        <Name>
        <ResponsiveText>
            {card.card_name}
          </ResponsiveText>
        </Name>
        <Cost>
        <ResponsiveText>
            {card.cost}
          </ResponsiveText>
        </Cost>
        <Description>
          <ResponsiveText>
            {card.description}
          </ResponsiveText>
        </Description>
        {card.card_type === 0 && (
          <>
            <Attack>
            <ResponsiveText>
                {card.attack}
              </ResponsiveText>
            </Attack>
            <Health>
            <ResponsiveText>
                {card.health}
              </ResponsiveText>
            </Health>
          </>
        )}
        <Class>
        <ResponsiveText>
            {card.card_class}
          </ResponsiveText>
        </Class>
      </CardFrame>
    </CardContainer>
  );
};

export default Card;

const CardContainer = styled.div`
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 3/4;
`;

const CardBase = styled.div`
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  background-repeat: no-repeat;
  background-size: contain;
  font-weight: bold;
`;

const CardFrame = styled(CardBase)`
  width: 100%;
  height: 100%;
  background-image: url(${frameImg});
`;

const CharacterFrame = styled(CardBase)`
  width: 92%;
  background-image: url(${characterFrameImg});
  top: 27%;
  left: 50%;
  transform: translate(-50%, -50%);
  aspect-ratio: 582/402;
`;

const Character = styled.img`
  position: absolute;
  top: 4%;
  width: 92%;
  box-sizing: border-box;
  aspect-ratio: 560/380;
  z-index: -1;
`;

const Name = styled(CardBase)`
  width: 69.84%;
  background-image: url(${nameImg});
  top: 47%;
  left: 50%;
  transform: translateX(-50%);
  aspect-ratio: 477/91;
  color: black;
`;

const Attack = styled(CardBase)`
  width: 21.9%;
  background-image: url(${attackImg});
  bottom: 3%;
  left: 3%;
  font-size: 6%;
  aspect-ratio: 138/165;
`;

const Health = styled(CardBase)`
  width: 23.49%;
  background-image: url(${healthImg});
  bottom: 2%;
  right: 2%;
  aspect-ratio: 156/163;
  font-size: 6%;
`;

const Cost = styled(CardBase)`
  width: 20.48%;
  background-image: url(${costImg});
  top: 2%;
  left: 2%;
  font-size: 6%;
  aspect-ratio: 1;
`;

const Description = styled(CardBase)`
  width: 92%;
  height: 33.5%; 
  background-image: url(${descriptionImg});
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
`;

const Class = styled(CardBase)`
  width: 52%;
  background-image: url(${classImg});
  bottom: 5%;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  aspect-ratio: 300/82;
`;
