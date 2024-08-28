import React, { useEffect, useState } from "react";
import { useRecoilState } from "recoil";
import {  isAuthenticatedState, loadingState } from "./atoms/global";
import {
  BrowserRouter,
  Route,
  Routes,
  useNavigate,
  Navigate,
} from "react-router-dom";
import styled from "styled-components";
import HomePage from "./pages/home/HomePage";
import LoginPage from "./pages/login/LoginPage";
import SignUpPage from "./pages/login/SignUp";
import SelectDeckPage from "./pages/deck/SelectDeckPage";
import ConfigDeckPage from "./pages/deck/ConfigDeckPage";
import PlayPage from "./pages/play/PlayPage";
import OptionPage from "./pages/option/OptionPage";
import useHttpUser from "./api/users";
import useHttpCard from "./api/cards";
import useHttpDeck from "./api/decks";
import ShowDeckPage from "./pages/deck/ShowDeckPage";

const App: React.FC = () => {
  const [loading, setLoading] = useRecoilState(loadingState);
  const navigate = useNavigate();
  const {  } = useHttpUser();
  const { getCards } = useHttpCard();
  const {authCheck, getUserStat, getUserCards, getUserDeckSelection } = useHttpUser();
  const [isAuthenticated, setIsAuthenticated] =
    useRecoilState(isAuthenticatedState);

  useEffect(() => {
    // 전체 페이지에서 우클릭 막기
    const handleContextMenu = (event: MouseEvent) => {
      event.preventDefault();
    };
    document.addEventListener("contextmenu", handleContextMenu);

    // 클린업 함수
    return () => {
      document.removeEventListener("contextmenu", handleContextMenu);
    };
  }, []);

  useEffect(() => {
    authCheck();
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      getUserStat();
      getUserCards();
      getCards();
      getUserDeckSelection();
    }
  }, [isAuthenticated]);

  if (isAuthenticated === null) {
    // 인증 상태를 확인 중일 때 로딩 화면을 표시
    return <div>Loading...</div>;
  }

  return (
    <Page className="App">
      <Routes>
        <Route
          path="/login"
          element={isAuthenticated ? <Navigate to="/" /> : <LoginPage />}
        />
        <Route
          path="/signup"
          element={isAuthenticated ? <Navigate to="/" /> : <SignUpPage />}
        />
        <Route
          path="/"
          element={isAuthenticated ? <HomePage /> : <Navigate to="/login" />}
        />
        <Route
          path="/play"
          element={isAuthenticated ? <PlayPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/option"
          element={isAuthenticated ? <OptionPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/deck"
          element={
            isAuthenticated ? <SelectDeckPage /> : <Navigate to="/login" />
          }
        />
        <Route
          path="/deck/:id"
          element={
            isAuthenticated ? <ShowDeckPage /> : <Navigate to="/login" />
          }
        />
      </Routes>
    </Page>
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
