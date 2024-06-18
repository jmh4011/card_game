import React, { useState } from "react";
import { useRecoilState, useRecoilValue } from "recoil";
import {PostDecks,GetDecks} from "../api/api";
import { decksState, userIdState } from "../atom";
import { styled } from "styled-components";

const ModalSeletDeck: React.FC = () => {
  const userId = useRecoilValue(userIdState)
  const [decks, setDecks] = useRecoilState(decksState)
  const [loading, setLoading] = useState(false)
  const [scale, setScale] = useState(.4)

  const handleCreate = () => {
    PostDecks(userId)
    GetDecks(userId,setDecks,setLoading)
  }

  const handleReset = () => {
    GetDecks(userId,setDecks,setLoading)
  }

  return <div>
    {loading? <div>
      loading
    </div>:<div>
      {decks.map((value,idx) => {
        return <Deck key={idx} scale={scale}>
          <DeckImg src={`/static/images/character/1.png`} scale={scale}/>
          <DeckName scale={scale}>{value.deck_name}</DeckName>
        </Deck>})}
      <button onClick={handleCreate}>create deck</button>
      <button onClick={handleReset}>reset</button>
    </div>}
  </div>
}

export default ModalSeletDeck



const Deck = styled.div<{ scale: number }>`
  margin-left: 5vw;
  margin-top: 5vh;
  display: inline-block;
  width: ${({ scale }) => 600 * scale}px;
  height: ${({ scale }) => 600 * scale}px;
  border: 1px solid rgb(0, 0, 0);
  text-align: center;
`

const DeckImg = styled.img<{ scale: number }>`
  width: ${({ scale }) => 560 * scale}px;
  height: ${({ scale }) => 380 * scale}px;
`

const DeckName = styled.div<{ scale: number }>`
  font-size: ${({ scale }) => 140 * scale}px;
`