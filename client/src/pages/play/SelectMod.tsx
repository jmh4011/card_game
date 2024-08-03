import React from "react";
import { useRecoilState } from "recoil";
import { showPageState } from "../../atoms/global";
import { playModState } from "../../atoms/play";

const SelectMod: React.FC = () => {
  const [showPage, setShowPage] = useRecoilState(showPageState)
  const [playMod, setPlayMod] = useRecoilState(playModState)

  const handleExit = () => {
    setShowPage("home")
  } 



  return <div>
    <button onClick={handleExit}>나가기</button>
    <div onClick={() => {setPlayMod("test")}}>테스트 플레이</div>
  </div>
}



export default SelectMod