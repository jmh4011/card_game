import React, { useState } from "react";
import { Socket } from "socket.io-client";
import useModal from "./useModal";
import {useSocketOn} from './Utiles'
import ModalCreateAccount from './ModalCreateAccount'
import { OutModal } from "./styles";
import styled from "styled-components";

interface ModalLoginPorps {
    closeModal: () => void
    socket : Socket
}



const ModalLogin: React.FC<ModalLoginPorps> = ({closeModal,socket}) => {
    const [userid, setUserid] = useState<String>()
    const [password,setPassword] = useState<String>()
    const send = () => {
        socket.emit('login', {userid : userid, password: password});
      };


    const {openModal:openModalCreateAccount,closeModal:closeModalCreateAccount} = useModal(() => 
        {return <ModalCreateAccount socket={socket} closeModal={closeModalCreateAccount} />})

    useSocketOn("login", (data) => {
        if(data === "Success") {
            closeModal()
        }
        else if (data === "useridError") {
            alert("존재하지 않는 아이디 입니다.")
        }
        else if (data === "passwordError") {
            alert("틀린 비밀번호")
        }
        else {
            alert("알 수 없는 오류 발생")
        }
    })
    return <>
    <OutModal/>
    <Login>
        <Cancel onClick={closeModal}>x</Cancel>
        <Title>Login</Title>
        <UserInput placeholder="id" type="text" onChange={(e) => {setUserid(e.target.value)}} />
        <UserInput placeholder="password" type="password" onChange={(e) => {setPassword(e.target.value)}} />
        <CreateAccount onClick={() => {closeModal(); openModalCreateAccount();}}>Create Account</CreateAccount>
        <LoginButton onClick={send}>완료</LoginButton>
    </Login>
    </>

    
}

const Login = styled.div`
    z-index: 15;
    border: 1px solid rgb(150, 150, 150);
    border-radius: 10px;
    background-color: white;
    width: 400px;
    height: 370px;
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
    margin-left: 50px;
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