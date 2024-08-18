import React, { useEffect, useState } from 'react';
import { useRecoilState } from 'recoil';
import { decksState, loadingState, showPageState} from './atoms/global';
import styled from 'styled-components';
import StartPage from './pages/start/StartPage';
import HomePage from './pages/home/HomePage';
import LoginPage from './pages/login/LoginPage';
import SignUpPage from './pages/login/SignUp';
import SelectDeckPage from './pages/deck/SelectDeckPage';
import ConfigDeckPage from './pages/deck/ConfigDeckPage';
import PlayPage from './pages/play/PlayPage';
import OptionPage from './pages/option/OptionPage';

const App: React.FC = () => {
  const [loading, setLoading] = useRecoilState(loadingState);
  const [decks, setDecks] = useRecoilState(decksState);
  const [showPage, setShowPage] = useRecoilState(showPageState);

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
          {showPage === "start" && <StartPage />}
          {showPage === "home" && <HomePage />}
          {showPage === "login" && <LoginPage />}
          {showPage === "signUp" && <SignUpPage />}
          {showPage === "selectDeck" && <SelectDeckPage />}
          {showPage === "configDeck" && <ConfigDeckPage />}
          {showPage === "play" && <PlayPage />}
          {showPage === "option" && <OptionPage />}
        </Page>
      )}
    </div>
  );
};



export type ShowPage = ('start' |"home" | "login" | 'signUp' | "selectDeck" | "configDeck" | "play" |"game" | 'option')

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
