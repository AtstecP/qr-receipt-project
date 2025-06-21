from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str


class UserInDB(BaseModel):
    email: str
    hashed_password: str
