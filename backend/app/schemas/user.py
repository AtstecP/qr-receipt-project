from pydantic import BaseModel, ConfigDict, Field, EmailStr, SecretStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    company_name: str
    email: EmailStr
    password: SecretStr

    model_config = ConfigDict(str_strip_whitespace=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr

    model_config = ConfigDict(str_strip_whitespace=True)