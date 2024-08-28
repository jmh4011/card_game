import React, { useState } from "react";
import { OutModal } from "../../utils/styles";
import styled from "styled-components";
import useHttpUser from "../../api/users";
import { useRecoilState, useSetRecoilState } from "recoil";
import { isAuthenticatedState, loadingState } from "../../atoms/global";
import { Link, useNavigate } from "react-router-dom";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const setLoading = useSetRecoilState(loadingState);

  const [isAuthenticated, setIsAuthenticated] =
    useRecoilState(isAuthenticatedState);
  const { userLogin } = useHttpUser();
  const navigate = useNavigate();

  const useHandleLogin = () => {
    userLogin(
      username,
      password,
      (data) => {
        setIsAuthenticated(true);
        navigate("/");
      },
      (data) => {
        alert("틀림");
      },
      setLoading
    );
  };

  return (
    <>
      <OutModal />
      <Login>
        <Title>Login</Title>
        <UserInput
          placeholder="id"
          type="text"
          onChange={(e) => setUsername(e.target.value)}
        />
        <UserInput
          placeholder="password"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <SignUp to={"/signup"}>Create Account</SignUp>
        <FindAccount onClick={() => navigate("/")}>Find Account</FindAccount>
        <LoginButton onClick={useHandleLogin}>완료</LoginButton>
      </Login>
    </>
  );
};

export default LoginPage;

const Login = styled.div`
  z-index: 15;
  border: 1px solid rgb(150, 150, 150);
  border-radius: 10px;
  background-color: rgb(255, 255, 255);
  width: 400px;
  height: 350px;
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
`;

const Title = styled.div`
  display: block;
  margin-left: 50px;
  margin-top: 30px;
  font-size: 35px;
  color: rgb(106, 36, 254);
`;

const UserInput = styled.input`
  display: block;
  margin-left: 50px;
  margin-top: 20px;
  width: 286px;
  height: 50px;
  border: 0;
  border-radius: 10px;
  outline: none;
  padding-left: 10px;
  background-color: rgb(233, 233, 233);
  font-size: 15px;
`;

const SignUp = styled(Link)`
  display: inline;
  margin-left: 50px;
  font-size: 15px;
  color: rgb(81, 121, 255);
  width: 110px;
  &:hover {
    text-decoration: underline;
    color: rgb(0, 60, 255);
  }
`;

const FindAccount = styled.p`
  display: inline;
  margin-left: 10px;
  font-size: 15px;
  color: rgb(81, 121, 255);
  width: 110px;
  &:hover {
    text-decoration: underline;
    color: rgb(0, 60, 255);
  }
`;

const LoginButton = styled.div`
  margin-left: 50px;
  width: 300px;
  height: 40px;
  color: rgb(255, 255, 255);
  font-size: 16px;
  background-color: rgb(106, 36, 254);
  text-align: center;
  line-height: 40px;
  margin-top: 20px;
  border-radius: 10px;
  &:hover {
    background-color: rgb(73, 26, 175);
  }
`;

const Cancel = styled.div`
  display: block;
  width: 20px;
  height: 20px;
  margin: 5px;
  float: right;
  font-size: 20px;
  text-align: center;
  line-height: 15px;
  color: rgb(100, 100, 100);
  border: 1px solid rgb(200, 200, 200);
  border-radius: 5px;
  &:hover {
    color: rgb(0, 0, 0);
  }
`;
