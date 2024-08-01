from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    fullname: str  

class OutputLogin(BaseModel):
    access_token: str
    token_type: str = "bearer"

class InputLogin(BaseModel):
    email: str
    password: str

