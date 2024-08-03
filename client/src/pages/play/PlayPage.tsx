import React from "react";
import { useRecoilState } from "recoil";
import { showPageState } from "../../atoms/global";
import { playModState } from "../../atoms/play";
import SelectMod from "./SelectMod";
import TestPlay from "./TestPlay";

export type PlayMod = null |"test"


const PlayPage: React.FC = () => {

  const [showPage, setShowPage] = useRecoilState(showPageState)
  const [playMod, setPlayMod] = useRecoilState(playModState)


  return <div>
    {playMod === null && <SelectMod/>}
    {playMod === "test" && <TestPlay/>}
  </div>
}


export default PlayPage