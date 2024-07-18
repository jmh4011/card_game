import React from "react";
import { useRecoilValue, useSetRecoilState } from "recoil";
import { cardsStats, decksState, loadingState, playerCardsStats, playerStats, showPageState} from "../../atoms/global";
import useHttpDeck from "../../api/decks";
import useHttpPlayer from "../../api/players";
import useHttpCard from "../../api/cards";


const ModalStart: React.FC = () => {
  const setDecks = useSetRecoilState(decksState)
  const setPlayer = useSetRecoilState(playerStats)
  const setShowPage = useSetRecoilState(showPageState)
  const setPlayerCards = useSetRecoilState(playerCardsStats)
  const setCards = useSetRecoilState(cardsStats)

  const {get} = useHttpCard()
  const {getDecks} = useHttpDeck()
  const {getPlayerState, getPlayerCards} = useHttpPlayer()

  const useHandleStart = () => {
    getDecks()

    getPlayerState(
      (data) => {setPlayer(data)}
    )

    getPlayerCards(
      (data) => {setPlayerCards(data)}
    )

    get(
      (data) => {setCards(data)}
    )

    setShowPage('main')
  }
return <div>
    <button onClick={useHandleStart}>start</button>
  </div>
}

export default ModalStart