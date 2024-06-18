import React, { useState } from "react";
import ModalCreateAccount from './ModalCreateAccount'
import { OutModal } from "../utile/styles";
import styled from "styled-components";
import {PostPlayer} from "../api/api";
import { useSetRecoilState } from "recoil";
import { showPageState, userIdState } from "../atom";

interface ModalLoginPorps {
}



const ModalLogin: React.FC<ModalLoginPorps> = () => {
  const [username, setUsernmae] = useState<string>('')
  const [password,setPassword] = useState<string>('')
  const setUserId = useSetRecoilState(userIdState)
  const setShowPage = useSetRecoilState(showPageState)


  const login = () => {
    PostPlayer(username, password, (data) => {
      if (data === -1){
        alert('틀림')
      }else{
        setUserId(data)
        setShowPage("main")
      }
    })
  }

  
  return <>
  <OutModal/>
  <Login>
    <Title>Login</Title>
    <UserInput placeholder="id" type="text" onChange={(e) => {setUsernmae(e.target.value)}} />
    <UserInput placeholder="password" type="password" onChange={(e) => {setPassword(e.target.value)}} />
    <CreateAccount onClick={() => {setShowPage("createAccount");}}>Create Account</CreateAccount>
    <FindAccount onClick={() => {alert("장민혁한테 문의하세요.")}}>Find Account</FindAccount>
    <LoginButton onClick={login}>완료</LoginButton>
  </Login>
  </>

    
}

const Login = styled.div`
    z-index: 15;
    border: 1px solid rgb(150, 150, 150);
    border-radius: 10px;
    background-color: white;
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
    color: #6A24FE;
`

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

const CreateAccount = styled.p`
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
    color: #fff;
    font-size: 16px;
    background-color: #6A24FE;
    text-align: center;
    line-height: 40px;
    margin-top: 20px;
    border-radius: 10px;
    &:hover {
        background-color: #491aaf;
      }
`
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
        color: rgb(0,0,0);
    }
`


export default ModalLogin