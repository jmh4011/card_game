import React from "react";
import MyHand from "../componenet/play/Myhand";
import { card } from "../utile/inter";
import Field from "../componenet/play/Field";

interface ModalGamePorps{
  player_id: number
}


const ModalGame : React.FC<ModalGamePorps> = ({player_id}) => {



  return <div>
    <Field/>
  </div>
}


export default ModalGame