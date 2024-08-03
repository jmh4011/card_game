import React from "react";
import { useRecoilValue, useSetRecoilState } from "recoil";
import { cardsStats, decksState, loadingState, userCardsStats, userStats, showPageState} from "../../atoms/global";
import useHttpDeck from "../../api/decks";
import useHttpUser from "../../api/users";
import useHttpCard from "../../api/cards";


const StartPage: React.FC = () => {
  const setDecks = useSetRecoilState(decksState)
  const setUser = useSetRecoilState(userStats)
  const setShowPage = useSetRecoilState(showPageState)
  const setUserCards = useSetRecoilState(userCardsStats)
  const setCards = useSetRecoilState(cardsStats)

  const {get} = useHttpCard()
  const {getDecks} = useHttpDeck()
  const {getUserState, getUserCards} = useHttpUser()

  const useHandleStart = () => {
    getDecks()

    getUserState(
      (data) => {setUser(data)}
    )

    getUserCards(
      (data) => {setUserCards(data)}
    )

    get(
      (data) => {setCards(data)}
    )

    setShowPage('home')
  }
return <div>
    <button onClick={useHandleStart}>start</button>
  </div>
}

export default StartPage;