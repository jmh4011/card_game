import React, { useState } from "react";
import { useRecoilState, useSetRecoilState } from "recoil";
import { loadingState, showPageState, wsTokenState} from "../../atoms/global";
import styled from "styled-components";
import useHttpUser from "../../api/users";
import useHttpDeck from "../../api/decks";
import useHttpGame from "../../api/game";


const HomePage: React.FC = () => {
  const [showPage, setShowPage] = useRecoilState(showPageState)
  const setLoading = useSetRecoilState(loadingState)
  const setWsToken = useSetRecoilState(wsTokenState)
  const {userLogout} = useHttpUser()
  const {getToken} = useHttpGame()
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

  const useHandleOption = () => {
    getToken((
      (data) => {
        setWsToken(data)
      } 
    ))
    setShowPage("option")
  }

  const useHandleLogout = () => {
    userLogout(
      (data) => {setShowPage("login")})
  }

  return <div>
    <button onClick={useHandlePlay}>플레이</button>
    <button onClick={useHandleDeck}>덱</button>
    <button onClick={useHandleShap}>상점</button>
    <button onClick={useHandleOption}>설정</button>
    <button onClick={useHandleLogout}>로그아웃</button>
  </div>
}

const Main = styled.div`

`


export default HomePage