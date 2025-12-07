from fastapi import APIRouter, status, HTTPException, Path
from src.models.news_model import News
from src.schemas.news_schema import NewsModel
from typing import Annotated
from src.auth.auth_utils import USER_DEPENDENCY
from src.database.database import DB_DEPENDENCY

news_router = APIRouter(
    prefix='/news',
    tags=['news']
)


@news_router.get('/', status_code=status.HTTP_200_OK)
async def get_all_news_from_platform(db: DB_DEPENDENCY, user: USER_DEPENDENCY):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    news_model = db.query(News).all()
    return news_model

@news_router.get('/{news_id}', status_code=status.HTTP_200_OK)
async def get_news(db: DB_DEPENDENCY, user: USER_DEPENDENCY, news_id: Annotated[int, Path(ge=1)]):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    news_model = db.query(News).filter(News.id == news_id).first()
    if not news_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Content not found')
    return news_model

