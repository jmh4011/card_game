import React, { useEffect, useState } from "react";
import { card } from "../utiles/inter";
import styled from "styled-components";
import { socket } from "../App";
import { useSocketOn } from "../utiles/Utiles";

 
interface CardProps {
    card: card;
    
}

class Card{
    id: number; 
    name: string;
    cost : number;
    attack : number;
    health : number;
    type : string;
    text : string;
    image : string;
    constructor(id:number){
        this.id = id
        socket.emit('card',id)
        useSocketOn('cardInfo', (data:any) => {
            (data);
        }); 
    }
}


// const Card: React.FC<CardProps> = ({card}) => {
//     useEffect(() => {
//     console.log(card)},[card])
//     return <CardStyled className="card">
//         <img src={require('../assets/image/base/attack.png')} alt="" />
//         <img src={require('../assets/image/base/card_frame.png')} alt="" />
//         <img src={require('../assets/image/base/character_frame.png')} alt="" />
//         <img src={require('../assets/image/base/cost.png')} alt="" />
//         <img src={require('../assets/image/base/health.png')} alt="" />
//         <img src={require('../assets/image/base/name.png')} alt="" />
//         <img src={require('../assets/image/base/text.png')} alt="" />
//         <img src={require('../assets/image/base/type.png')} alt="" />
//         {card.attack}
//     </CardStyled>
// }




export default Card


const CardStyled =  styled.div`
    border: 1px solid black;
`


