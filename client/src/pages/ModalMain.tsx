import React from "react";
import { useRecoilState } from "recoil";
import { showPageState, userIdState } from "../atom";
import styled from "styled-components";


const ModalMain: React.FC = () => {
  const [showPage, setShowPage] = useRecoilState(showPageState)
  const [userId,SerUserId] = useRecoilState(userIdState)

  const handlePlay = () => {
    alert("미구현")
  }

  const handleDeck = () => {
    setShowPage("seletDeck")
  }

  const handleShap = () => {
    alert("미구현")
  }

  const handleSetting = () => {
    alert("미구현")
  }

  const handleLogout = () => {
    SerUserId(0)
    setShowPage("login")
  }

  return <div>
    <button onClick={handlePlay}>플레이</button>
    <button onClick={handleDeck}>덱</button>
    <button onClick={handleShap}>상점</button>
    <button onClick={handleSetting}>설정</button>
    <button onClick={handleLogout}>로그아웃</button>
  </div>
}

const Main = styled.div`

`


export default ModalMain