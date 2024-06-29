import React from "react";
import { card } from "../utils/inter";
import styled from "styled-components";
import baseSprites from '../assets/base_sprites.png';

interface CardProps {
  card: card;
  scale: number;
}

const Card: React.FC<CardProps> = ({ card, scale }) => {
  return (
    <CardContainer scale={scale}>
      <CardFrame scale={scale}>
        <Character src={`/static/images/character/${card.image}`} alt="" scale={scale} />
        <CharacterFrame scale={scale} />
        <Name scale={scale}>{card.card_name}</Name>
        <Cost scale={scale}>{card.cost}</Cost>
        <Text scale={scale}>{card.description}</Text>
        {card.card_type === 0 && (
          <>
            <Attack scale={scale}>{card.attack}</Attack>
            <Health scale={scale}>{card.health}</Health>
          </>
        )}
        <Type scale={scale}>{card.card_class}</Type>
      </CardFrame>
    </CardContainer>
  );
};

export default Card;

const CardContainer = styled.div<{ scale: number }>`
  position: relative;
  width: ${({ scale }) => 630 * scale}px;
  height: ${({ scale }) => 830 * scale}px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const IconLink = styled.div<{ scale: number }>`
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  background-image: url(${baseSprites});
  background-repeat: no-repeat;
  background-size: ${({ scale }) => 1410 * scale}px ${({ scale }) => 1135 * scale}px;
  font-weight: bold;
`;

const CardFrame = styled(IconLink)`
  width: ${({ scale }) => 630 * scale}px;
  height: ${({ scale }) => 830 * scale}px;
  background-position: ${({ scale }) => -10 * scale}px ${({ scale }) => -10 * scale}px;
`;

const CharacterFrame = styled(IconLink)`
  width: ${({ scale }) => 582 * scale}px;
  height: ${({ scale }) => 402 * scale}px;
  background-position: ${({ scale }) => -660 * scale}px ${({ scale }) => -10 * scale}px;
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

const Character = styled.img<{ scale: number }>`
  position: absolute;
  width: ${({ scale }) => 560 * scale}px;
  height: ${({ scale }) => 380 * scale}px;
  top: 27%;
  left: 50%;
  transform: translate(-50%, -50%);
`;

const Name = styled(IconLink)`
  width: ${({ scale }) => 440 * scale}px;
  height: ${({ scale }) => 89 * scale}px;
  background-position: ${({ scale }) => -660 * scale}px ${({ scale }) => -726 * scale}px;
  top: 47%;
  left: 50%;
  transform: translateX(-50%);
  color: black;
  font-size: ${({ scale, children }) => {
    const length = (children as string).length;
    return length < 15 ? `${60 * scale}px` : `${30 * scale}px`; // Adjust font size based on length
  }};
`;

const Attack = styled(IconLink)`
  width: ${({ scale }) => 138 * scale}px;
  height: ${({ scale }) => 165 * scale}px;
  background-position: ${({ scale }) => -1262 * scale}px ${({ scale }) => -10 * scale}px;
  bottom: 3%;
  left: 3%;
  font-size: ${({ scale }) => 100 * scale}px;
`;

const Health = styled(IconLink)`
  width: ${({ scale }) => 148 * scale}px;
  height: ${({ scale }) => 163 * scale}px;
  background-position: ${({ scale }) => -10 * scale}px ${({ scale }) => -962 * scale}px;
  bottom: 2%;
  right: 2%;
  font-size: ${({ scale }) => 100 * scale}px;
`;

const Cost = styled(IconLink)`
  width: ${({ scale }) => 129 * scale}px;
  height: ${({ scale }) => 129 * scale}px;
  background-position: ${({ scale }) => -1262 * scale}px ${({ scale }) => -195 * scale}px;
  top: 2%;
  left: 2%;
  font-size: ${({ scale }) => 100 * scale}px;
`;

const Text = styled(IconLink)`
  width: ${({ scale }) => 582 * scale}px;
  height: ${({ scale }) => 274 * scale}px;
  background-position: ${({ scale }) => -660 * scale}px ${({ scale }) => -432 * scale}px;
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
  font-size: ${({ scale, children }) => {
    const length = (children as string).length;
    return length < 50 ? `${50 * scale}px` : `${30 * scale}px`; // Adjust font size based on length
  }};
`;

const Type = styled(IconLink)`
  width: ${({ scale }) => 332 * scale}px;
  height: ${({ scale }) => 82 * scale}px;
  background-position: ${({ scale }) => -10 * scale}px ${({ scale }) => -860 * scale}px;
  bottom: 5%;
  left: 50%;
  transform: translateX(-50%);
  font-size: ${({ scale }) => 50 * scale}px;
`;
