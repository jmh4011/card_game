import React from "react";
import { useRecoilValue, useSetRecoilState } from "recoil";
import { decksState, loadingState, playerCardsStats, playerStats, showPageState, userIdState } from "../../atoms/global";
import { GetDecks } from "../../api/decks";
import { GetPlayer, GetPlayerCards } from "../../api/players";


const ModalStart: React.FC = () => { 
  const userId = useRecoilValue(userIdState)
  const setDecks = useSetRecoilState(decksState)
  const setPlayer = useSetRecoilState(playerStats)
  const setShowPage = useSetRecoilState(showPageState)
  const setPlayerCards = useSetRecoilState(playerCardsStats)
  const setLoading = useSetRecoilState(loadingState)


  const handleStart = () => {
    GetDecks(userId, setDecks,setLoading)
    GetPlayer(userId, setPlayer, setLoading)
    GetPlayerCards(userId, setPlayerCards, setLoading)
    setShowPage('main')
  }
return <div>
    <button onClick={handleStart}>start</button>
  </div>
}

export default ModalStart