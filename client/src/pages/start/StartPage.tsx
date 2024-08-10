import React from "react";
import { useRecoilValue, useSetRecoilState } from "recoil";
import { cardsStats, decksState, loadingState, userCardsStats, userStats, showPageState, deckSelectionState} from "../../atoms/global";
import useHttpDeck from "../../api/decks";
import useHttpUser from "../../api/users";
import useHttpCard from "../../api/cards";


const StartPage: React.FC = () => {
  const setDecks = useSetRecoilState(decksState)
  const setUser = useSetRecoilState(userStats)
  const setShowPage = useSetRecoilState(showPageState)
  const setUserCards = useSetRecoilState(userCardsStats)
  const setCards = useSetRecoilState(cardsStats)
  const setDeckSelection = useSetRecoilState(deckSelectionState)


  const {getCards} = useHttpCard()
  const {getDecks} = useHttpDeck()
  const {getUserStat, getUserCards, getUserDeckSelection} = useHttpUser()

  const useHandleStart = () => {
    getDecks()

    getUserStat(
      (data) => {setUser(data)}
    )

    getUserCards(
      (data) => {setUserCards(data)}
    )

    getCards(
      (data) => {setCards(data)}
    )

    getUserDeckSelection(
      (data) => {setDeckSelection(data)}
    )

    setShowPage('home')
  }
return <div>
    <button onClick={useHandleStart}>start</button>
  </div>
}

export default StartPage;