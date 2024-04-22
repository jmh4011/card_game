import React, { useEffect } from 'react';
import io from 'socket.io-client';
import ModalLogin from './components/ui/ModalLogin';
import useModal from './components/utiles/useModal';
import { useSocketOn } from './components/utiles/Utiles';


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
