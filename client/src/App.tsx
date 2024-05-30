import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import ModalLogin from './pages/ModalLogin';
import useModal from './utile/useModal';
import { useSocketOn} from './utile/Utiles';
import Card from './components/Card'

export const socket = io("ws://localhost:5000");

function App() {
  const sendMessage = () => {
    socket.emit('message', 'Hello World!');
  };
  useSocketOn('message', (data) => {console.log(data)})


  const {openModal:openModalLogin,closeModal:closeModalLogin} = useModal(() => 
    {return <ModalLogin socket={socket} closeModal={closeModalLogin} />})


  return (
    <div className="App">
      <button onClick={sendMessage}>sned message</button>
      <button onClick={openModalLogin}>login</button>
    </div>
  );
}

export default App;
