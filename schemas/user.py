from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    is_active:bool=Field(default=True)

class UserResponse(UserCreate):
    id:int

    class Config:
        from_attributes=True

class UserQuery(BaseModel):
    name : str
    email:EmailStr
    is_active:bool