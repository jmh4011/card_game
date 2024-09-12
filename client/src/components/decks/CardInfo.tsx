import React from "react";
import { useRecoilValue } from "recoil";
import styled from "styled-components";
import {
  cardsStats,
  effectsStats,
  userCardsStats,
} from "../../atoms/global";
import { characterImage } from "../../api/static";
import ResponsiveText from "../ResponsiveText";
import ResDescription from "../ResDescription";
import ScrollableDescription from "../ScrollableDescription";
import { CardDescription } from "../ShowCard";

interface CardInfoProps {
  card_id: number;
  deckCount: number;
}

const CardInfo: React.FC<CardInfoProps> = ({ card_id, deckCount }) => {
  const card = useRecoilValue(cardsStats)[card_id];
  const userCount = useRecoilValue(userCardsStats)[card_id];
  const effects = useRecoilValue(effectsStats);

  return (
    <InfoContainer>
      <CardId>{card.card_id}</CardId>
      <Name>
        <ResponsiveText>{card.card_name}</ResponsiveText>
      </Name>
      <Image src={characterImage(card.image_path)} alt={card.card_name} />
      <Attack>
        <ResponsiveText>{card.attack}</ResponsiveText>
      </Attack>
      <Health>
        <ResponsiveText>{card.health}</ResponsiveText>
      </Health>
      <Class>
        <ResponsiveText>{card.card_class}</ResponsiveText>
      </Class>
      <Description>
        <ScrollableDescription>{CardDescription(card)}</ScrollableDescription>
      </Description>

      <UserCount>
        <ResponsiveText>{userCount || 0}</ResponsiveText>
      </UserCount>
      <DeckCount>
        <ResponsiveText>{deckCount || 0}</ResponsiveText>
      </DeckCount>
    </InfoContainer>
  );
};

export default CardInfo;

const InfoContainer = styled.div`
  height: 100%;
`;

const CardId = styled.div`
  font-size: 0.1%;
`;

const Name = styled.div`
  width: 90%;
  margin-left: 5%;
  border: 1px solid rgb(0, 0, 0);
`;

const Image = styled.img`
  width: 80%;
  aspect-ratio: 560 / 380; /* 3:4 비율 고정 */
  margin-top: 2%;
  margin-left: 10%;
  margin-right: 10%;
  border: 1px solid rgb(0, 0, 0);
  border-radius: 10px;
`;

const Stat = styled.div`
  display: inline-block;
  border: 1px solid rgb(0, 0, 0);
  border-radius: 10px;
  width: 40%;
  text-align: center;
  margin-left: 5%;
  height: 4%;
`;

const Attack = styled(Stat)`
  background-color: rgb(255, 255, 0);
`;

const Health = styled(Stat)`
  background-color: rgb(255, 0, 0);
`;

const Class = styled.div`
  color: rgb(0, 0, 0);
  width: 100%;
  height: 4%;
  text-align: center;
`;

const Description = styled.div`
  overflow: auto;
  max-width: 100%;
  height: 30%;
  width: 90%;
  border: 1px solid rgb(0, 0, 0);
  border-radius: 10px;
  margin-left: 5%;

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

const UserCount = styled.div`
  display: inline-block;
  border: 1px solid rgb(0, 0, 0);
  border-radius: 10px;
  width: 40%;
  text-align: center;
  margin-left: 7%;
  height: 4%;
`;

const DeckCount = styled.div`
  display: inline-block;
  border: 1px solid rgb(0, 0, 0);
  border-radius: 10px;
  width: 40%;
  text-align: center;
  margin-left: 5%;
  height: 4%;
`;
