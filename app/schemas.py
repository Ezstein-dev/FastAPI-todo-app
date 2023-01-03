from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from fastapi import openapi




class TodoIn(BaseModel):
    
    due_date: date
    description: str
    published: bool = True

class Todo(TodoIn):

    id: int
    created_at: datetime

    class Config: 
        orm_mode = True

class UserIn(BaseModel):

    username: str
    email: EmailStr
    password: str

class User(UserIn):

    id: int
    created_at: datetime

    class Config: 
        orm_mode = True

class Token(BaseModel): 
    access_token: str 
    token_type: str

class TokenData(BaseModel): 
    id: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str