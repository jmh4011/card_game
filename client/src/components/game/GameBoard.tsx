import React, { useState } from "react";


const GameBoard: React.FC = () => {

    const [hand,setHand] = useState(1)

    return <div>
        <div className="player-hand">
        </div>
        <div className="enemy-hand">
        </div>
    </div>
}


export default GameBoard