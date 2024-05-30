import classnames from "classnames"
import { useEffect, useState } from "react"
import { styleVibration, useSocketOn } from "../utile/Utiles"
import { Socket } from "socket.io-client"
import styled, { css } from 'styled-components';
import { OutModal, Vibration } from "../utile/styles";


interface ModalLoginPorps {
    closeModal: () => void
    socket : Socket
}


const ModalCreateAccount: React.FC<ModalLoginPorps> = ({closeModal,socket}) => {
    const [userid, setUserid] = useState<String>('')
    const [password,setPassword] = useState<String>('')
    const [againPassword,setAgainPassword] = useState<String>('')
    const [vibration, setVibration] = useState<boolean>(false)

    const send = () => {
        if (password !== againPassword) {
            setVibration(true)
        }
        else {
            socket.emit('create_account', {userid : userid, password: password});
        }
    };
    
    useSocketOn("create_account", (data) => {
        if(data === "success") {
            closeModal()
            alert("계정 생성됨")
        }
        else if (data === "useridDuplicate") {
            alert("이미 존재하는 아이디 입니다.")
        }
        else {
            alert("알 수 없는 오류 발생")
        }
    })
    useEffect(() => {
        if (vibration) {
            const timer = setTimeout(() => setVibration(false), 400);
            return () => clearTimeout(timer);
        }
    }, [vibration]);

    return <>
    <OutModal/>
    <CreateAccount>
        <Cancel onClick={closeModal}>x</Cancel>
        <Title>create account</Title>
        <UserInput placeholder="id" type="text" onChange={(e) => {setUserid(e.target.value)}} />
        <UserInput placeholder="new Password" type="password" onChange={(e) => {setPassword(e.target.value)}} />
        <UserInput placeholder="again Password" type="password" onChange={(e) => {setAgainPassword(e.target.value)}} />
        {password !== againPassword && vibration && <WeakInput>비밀번호가 일치 하지 않습니다.</WeakInput>}
        <LoginButton onClick={send}>완료</LoginButton>
    </CreateAccount>
    </>
}

const CreateAccount = styled.div`
    z-index: 15;
    border: 1px solid rgb(150, 150, 150);
    border-radius: 10px;
    background-color: white;
    width: 400px;
    height: 400px;
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

const WeakInput = styled.p`
    margin-left: 50px;
    font-size: 10px;
    color: red;
    animation: ${Vibration} 0.4s infinite;
`;


export default ModalCreateAccount