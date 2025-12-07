from fastapi import APIRouter, status, HTTPException, Depends
from src.models.users_model import Users
from src.schemas.users_schema import UserModel, UserResponseModel
from src.database.database import DB_DEPENDENCY
from src.auth.auth_utils import pwd_context, authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta



auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@auth_router.post('/create-user', status_code=status.HTTP_201_CREATED)
async def create_user(db: DB_DEPENDENCY, user_request: UserModel):
    user_model = Users(**user_request.model_dump(exclude={'password'}))
    user_model.hashed_password = pwd_context.hash(user_request.password)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login_for_access_token(db: DB_DEPENDENCY, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_access_token(user.email, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
    

