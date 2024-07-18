import React from "react";
import { useRecoilState } from "recoil";
import { showPageState } from "../../atoms/global";

export type PlayMod = "test"


const ModalPlay: React.FC = () => {

  const [showPage, setShowPage] = useRecoilState(showPageState)

  const handleExit = () => {
    setShowPage("main")
  } 



  return <div>
    <button onClick={handleExit}>나가기</button>
    <div onClick={() => {}}>테스트 플레이</div>
  </div>
}


export default ModalPlay