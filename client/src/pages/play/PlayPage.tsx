import React from "react";
import { useRecoilState } from "recoil";
import { showPageState } from "../../atoms/global";
import SelectMod from "./components/SelectMod";
import TestPlay from "./TestPlay";

export type PlayMod = null |"test"


const PlayPage: React.FC = () => {

  const [showPage, setShowPage] = useRecoilState(showPageState)


  return <div>

  </div>
}


export default PlayPage