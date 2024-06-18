import React, { useEffect, useState } from 'react';
import { useUserIdSync } from './utile/cookie';
import { useRecoilState } from 'recoil';
import { decksState, showPageState, userIdState } from './atom';
import ModalMain from './pages/ModalMain';
import ModalLogin from './pages/ModalLogin';
import ModalCreateAccount from './pages/ModalCreateAccount';
import ModalSeletDeck from './pages/ModalSeletDeck';


const App: React.FC = () => {
  const [userId, setUserId] = useRecoilState(userIdState);
  const [decks, setDecks] = useRecoilState(decksState);
  const [showPage, setShowPege] = useRecoilState(showPageState)
  useUserIdSync()


  return (
    <div className="App">
      <div></div>
      
      {showPage === 'main'?
      <ModalMain/>:null}

      {showPage === 'login'?
      <ModalLogin/>:null}
      
      {showPage === 'createAccount'?
      <ModalCreateAccount/>:null}
      
      {showPage === 'seletDeck'?
      <ModalSeletDeck/>:null}
      
    </div>
  );
}

export default App;
