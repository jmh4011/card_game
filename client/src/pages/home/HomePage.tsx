import React, { useState } from "react";
import { useRecoilState, useSetRecoilState } from "recoil";
import {
  isAuthenticatedState,
  loadingState,
  wsTokenState,
} from "../../atoms/global";
import styled from "styled-components";
import useHttpUser from "../../api/users";
import useHttpDeck from "../../api/decks";
import useHttpGame from "../../api/game";
import { useNavigate } from "react-router-dom";

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const setLoading = useSetRecoilState(loadingState);
  const setWsToken = useSetRecoilState(wsTokenState);
  const { userLogout } = useHttpUser();
  const { getToken } = useHttpGame();
  const {} = useHttpDeck;
  const [isAuthenticated, setIsAuthenticated] =
    useRecoilState(isAuthenticatedState);

  const handlePlay = () => {
    navigate("/play");
  };

  const handleDeck = () => {
    navigate("/deck");
  };

  const handleShap = () => {
    alert("미구현");
  };

  const handleOption = () => {
    getToken((data) => {
      setWsToken(data);
    });
    navigate("/option");
  };

  const handleLogout = () => {
    userLogout((data) => {
      setIsAuthenticated(false);
      navigate("/login");
    });
  };

  return (
    <div>
      <button onClick={handlePlay}>플레이</button>
      <button onClick={handleDeck}>덱</button>
      <button onClick={handleShap}>상점</button>
      <button onClick={handleOption}>설정</button>
      <button onClick={handleLogout}>로그아웃</button>
    </div>
  );
};

const Main = styled.div``;

export default HomePage;
