import React, { useState } from "react";
import styled from "styled-components";
import attackImg from "../assets/card-base/attack.png";
import characterFrameImg from "../assets/card-base/character-frame.png";
import classImg from "../assets/card-base/class.png";
import descriptionImg from "../assets/card-base/description.png";
import frameImg from "../assets/card-base/frame.png";
import healthImg from "../assets/card-base/health.png";
import nameImg from "../assets/card-base/name.png";
import { useRecoilValue } from "recoil";
import { cardsStats } from "../atoms/global";
import { characterImage } from "../api/static";
import ResponsiveText from "./ResponsiveText";
import ResDescription from "./ResDescription";

interface CardProps {
  card_id: number;
}

const Card: React.FC<CardProps> = ({ card_id }) => {
  const card = useRecoilValue(cardsStats)[card_id];

  return (
    <CardContainer>
      <CardFrame>
        <Character src={characterImage(card.image_path)} />
        <Name>
          <ResponsiveText>{card.card_name}</ResponsiveText>
        </Name>
        <Description>
          <ResDescription>
            {card.description}
          </ResDescription>
        </Description>
        {card.card_type === 0 && (
          <>
            <Attack>
              <ResponsiveText>{card.attack}</ResponsiveText>
            </Attack>
            <Health>
              <ResponsiveText>{card.health}</ResponsiveText>
            </Health>
          </>
        )}
        <Class>
          <ResponsiveText>{card.card_class}</ResponsiveText>
        </Class>
      </CardFrame>
    </CardContainer>
  );
};

export default Card;

const CardContainer = styled.div`
  box-sizing: border-box;
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 3/4;
  background-color: rgb(255,255,255);
  z-index: -20;
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
  width: 92.1%;
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
  border-radius: 4px;
  border: 1px solid rgb(0, 0, 0);
  z-index: -1;
`;

const Name = styled(CardBase)`
  width: 69.84%;
  background-image: url(${nameImg});
  top: 47%;
  left: 50%;
  transform: translateX(-50%);
  aspect-ratio: 477/91;
`;

const Attack = styled(CardBase)`
  width: 21.9%;
  background-image: url(${attackImg});
  bottom: 3%;
  left: 3%;
  aspect-ratio: 138/165;
`;

const Health = styled(CardBase)`
  width: 23.49%;
  background-image: url(${healthImg});
  bottom: 2%;
  right: 2%;
  aspect-ratio: 156/163;
`;

const Description = styled(CardBase)`
  width: 92%;
  height: 33.5%;
  background-image: url(${descriptionImg});
  bottom: 10%;
  white-space: pre-wrap; 
`;

const Class = styled(CardBase)`
  width: 52%;
  background-image: url(${classImg});
  bottom: 5%;
  aspect-ratio: 300/82;
`;

