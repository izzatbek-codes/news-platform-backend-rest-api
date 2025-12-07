from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    is_active: bool

class UserModel(UserBase):
    password: Annotated[str, Field(min_length=8, max_length=16)]

    
class UserResponseModel(UserModel):
    id: int
    registered_at: datetime

    class Config:
        from_attributes = True


class ChangeUsersPasswordRequest(BaseModel):
    current_password: Annotated[str, Field(min_length=8, max_length=16)]
    new_password: Annotated[str, Field(min_length=8, max_length=16)]
    new_password_repeat: Annotated[str, Field(min_length=8, max_length=16)]
        