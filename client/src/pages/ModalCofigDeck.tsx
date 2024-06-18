import React, { useState } from "react";
import { useRecoilState } from "recoil";
import { userIdState } from "../atom";
import apiManager from "../api/api";

const ModalCofingDeck: React.FC = () => {
  const userId = useRecoilState(userIdState)

  
  return <div>

    <button>create deck</button>
  </div>
}

export default ModalCofingDeck