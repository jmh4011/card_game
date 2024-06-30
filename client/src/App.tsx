import React, { useEffect, useState } from 'react';
import { useUserIdSync } from './utils/cookie';
import { useRecoilState } from 'recoil';
import { decksState, loadingState, showPageState, userIdState } from './atoms/global';
import ModalMain from './pages/modals/ModalMain';
import ModalLogin from './pages/modals/ModalLogin';
import ModalCreateAccount from './pages/modals/ModalCreateAccount';
import ModalSelectDeck from './pages/modals/ModalSelectDeck';
import ModalConfigDeck from './pages/modals/ModalConfigDeck';
import styled from 'styled-components';
import ModalStart from './pages/modals/ModalStart';

const App: React.FC = () => {
  const [userId, setUserId] = useRecoilState(userIdState);
  const [loading, setLoading] = useRecoilState(loadingState);
  const [decks, setDecks] = useRecoilState(decksState);
  const [showPage, setShowPage] = useRecoilState(showPageState);
  useUserIdSync();

  useEffect(() => {
    // 전체 페이지에서 우클릭 막기
    const handleContextMenu = (event: MouseEvent) => {
      event.preventDefault();
    };
    document.addEventListener('contextmenu', handleContextMenu);

    // 클린업 함수
    return () => {
      document.removeEventListener('contextmenu', handleContextMenu);
    };
  }, []);

  return (
    <div className="App">
      {loading ? (
        <LoadingScreen>Loading...</LoadingScreen>
      ) : (
        <Page>
          {showPage === "start" && <ModalStart />}
          {showPage === "main" && <ModalMain />}
          {showPage === "login" && <ModalLogin />}
          {showPage === "createAccount" && <ModalCreateAccount />}
          {showPage === "selectDeck" && <ModalSelectDeck />}
          {showPage === "configDeck" && <ModalConfigDeck />}
        </Page>
      )}
    </div>
  );
};

const Page = styled.div`
  width: 100vw;
  height: 100vh;
`;

const LoadingScreen = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100vw;
  height: 100vh;
  font-size: 24px;
`;

export default App;
