from fastapi import APIRouter, status, HTTPException, Path
from src.models.news_model import News
from typing import Annotated
from src.auth.auth_utils import USER_DEPENDENCY
from src.database.database import DB_DEPENDENCY
from src.models.users_model import Users


admin_router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

@admin_router.delete('/delete-content/{news_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_content_by_admin(db: DB_DEPENDENCY, user: USER_DEPENDENCY, news_id: Annotated[int, Path(ge=1)]):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    content_model = db.query(News).filter(News.id == news_id).first()
    if not content_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Content not found')
    db.delete(content_model)
    db.commit()

@admin_router.delete('/delete-user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_admin(db: DB_DEPENDENCY, user: USER_DEPENDENCY, user_id: Annotated[int, Path(ge=1)]):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    user_model = db.query(Users).filter(Users.id == user_id).first()
    if not user_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    db.delete(user_model)
    db.commit()

