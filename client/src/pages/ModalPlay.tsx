import React from "react";
import MyHand from "../components/play/Myhand";
import { card } from "../utils/inter";
import Field from "../components/play/Field";

interface ModalGamePorps{
  player_id: number
}


const ModalGame : React.FC<ModalGamePorps> = ({player_id}) => {



  return <div>
    <Field/>
  </div>
}


export default ModalGame