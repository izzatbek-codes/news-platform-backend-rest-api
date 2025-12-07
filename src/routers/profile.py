from fastapi import APIRouter, status, HTTPException, Path
from src.models.news_model import News
from typing import Annotated
from src.auth.auth_utils import USER_DEPENDENCY
from src.database.database import DB_DEPENDENCY
from src.models.users_model import Users
from src.schemas.users_schema import ChangeUsersPasswordRequest
from src.auth.auth_utils import pwd_context

profile_router = APIRouter(
    prefix='/profile',
    tags=['profile']
)

@profile_router.get('/get-profile-data', status_code=status.HTTP_200_OK)
async def profile_datas(db: DB_DEPENDENCY, user: USER_DEPENDENCY):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not user_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user_model


@profile_router.put('/change-password', status_code=status.HTTP_204_NO_CONTENT)
async def change_user_password(db: DB_DEPENDENCY, user: USER_DEPENDENCY, password_request: ChangeUsersPasswordRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not user_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if not pwd_context.verify(password_request.current_password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect current password')
    if password_request.new_password != password_request.new_password_repeat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Could not confirm new password')
    user_model.hashed_password = pwd_context.hash(password_request.new_password)
    db.commit()

@profile_router.delete('/delete-profile/{password}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(db: DB_DEPENDENCY, user: USER_DEPENDENCY, password: Annotated[str, Path(min_length=8, max_length=16)]):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not user_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if not pwd_context.verify(password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')
    db.delete(user_model)
    db.commit()


    
