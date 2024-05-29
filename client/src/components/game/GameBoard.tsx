import React, { useState } from "react";
import { card } from "../../utiles/inter";


const GameBoard: React.FC = () => {

    const [hand,setHand] = useState<card[]>()

    return <div>
        
        <div className="player-hand">
        
        </div>
        
        <div className="enemy-hand">
        
        </div>
    </div>
}


export default GameBoard