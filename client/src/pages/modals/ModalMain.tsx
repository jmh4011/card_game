import React from "react";
import { useRecoilState, useSetRecoilState } from "recoil";
import { loadingState, showPageState} from "../../atoms/global";
import styled from "styled-components";
import useHttpPlayer from "../../api/players";
import useHttpDeck from "../../api/decks";
import Card from "../../components/Card";


const ModalMain: React.FC = () => {
  const [showPage, setShowPage] = useRecoilState(showPageState)
  const setLoading = useSetRecoilState(loadingState)
  const {playerLogout} = useHttpPlayer()
  const {} = useHttpDeck

  const useHandlePlay = () => {
    alert("미구현")
  }

  const useHandleDeck = () => {
    setShowPage("selectDeck")
  }

  const useHandleShap = () => {
    alert("미구현")
  }

  const useHandleSetting = () => {
    alert("미구현")
  }

  const useHandleLogout = () => {
    playerLogout(
      (data) => {setShowPage("login")})
  }

  return <div>
    <button onClick={useHandlePlay}>플레이</button>
    <button onClick={useHandleDeck}>덱</button>
    <button onClick={useHandleShap}>상점</button>
    <button onClick={useHandleSetting}>설정</button>
    <button onClick={useHandleLogout}>로그아웃</button>
  </div>
}

const Main = styled.div`

`


export default ModalMain