import React from "react";
import { player_card } from "../../utils/inter";
import styled from "styled-components";

interface CardInfoProps {
  card: player_card;
}

const CardInfo: React.FC<CardInfoProps> = ({ card }) => {
  return (
    <InfoContainer>
      <CardId>{card.card_id}</CardId>
      <Name>{card.card_name}</Name>
      <Image src={`/static/images/character/${card.image}`} alt={card.card_name} />
      <Cost>{card.cost}</Cost>
      <Attack>{card.attack}</Attack>
      <Health>{card.health}</Health>
      <Class>{card.card_class}</Class>
      <Description>{card.description}</Description>
    </InfoContainer>
  );
};

export default CardInfo;

const InfoContainer = styled.div`
  width: 100%;
  height: 100%;
`;

const CardId = styled.div`
  font-size: 0.1%;
`;

const Name = styled.div`
  font-size: 2vw;
  width: 90%;
  margin-left: 5%;
  border: 1px solid rgb(0, 0, 0);
`;

const Image = styled.img`
  width: 80%;
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
  width: 25%;
  text-align: center;
  margin-left: 5%;
`;

const Cost = styled(Stat)`
  background-color: rgb(0, 150, 255);
`;

const Attack = styled(Stat)`
  background-color: rgb(255, 255, 0);
`;

const Health = styled(Stat)`
  background-color: rgb(255, 0, 0);
`;

const Class = styled.div`
  color: rgb(0, 0, 0);
`;

const Description = styled.div`
  overflow: auto;
  max-width: 100%;
  height: 40%;
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
