from pydantic import BaseModel
from schemas.game.player_info import PlayerInfo

class GameInfo(BaseModel):
    Player: PlayerInfo
    opponent: PlayerInfo
    turn: int
    is_player_turn: bool
    side_effects: list[int] = []

    class Config:
        use_enum_values = True
