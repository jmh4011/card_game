from pydantic import BaseModel


class RouterUserStatUpdate(BaseModel):
    money: int | None
    nickname: str | None
    current_mod_id: int | None
