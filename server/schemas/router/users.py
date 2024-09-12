from pydantic import BaseModel
from schemas.db.users import UserBase

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserSignUp(BaseModel):
    username: str
    password: str
    again_password: str