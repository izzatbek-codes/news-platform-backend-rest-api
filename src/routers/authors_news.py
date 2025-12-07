from fastapi import APIRouter, status, HTTPException, Path
from src.models.news_model import News
from src.schemas.news_schema import NewsModel
from typing import Annotated
from src.auth.auth_utils import USER_DEPENDENCY
from src.database.database import DB_DEPENDENCY

author_router = APIRouter(
    prefix='/authors',
    tags=['authors']
)

@author_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_content(db: DB_DEPENDENCY, user: USER_DEPENDENCY, news_schema: NewsModel):
    if not user or user.get('role') != 'author':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    content_model = News(**news_schema.model_dump(), owner_id = user.get('id'))
    db.add(content_model)
    db.commit()
    db.refresh(content_model)
    return content_model

@author_router.put('/{news_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_authors_content(db: DB_DEPENDENCY, user: USER_DEPENDENCY,
                                  news_schema: NewsModel, news_id: Annotated[int, Path(ge=1)]):
    if not user or user.get('role') != 'author':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    content_model = db.query(News).filter(News.id == news_id).filter(News.owner_id == user.get('id')).first()
    if not content_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Content not found')
    content_schema_json = news_schema.model_dump()
    for keys, values in content_schema_json.items():
        setattr(content_model, keys, values)

    db.commit()

@author_router.delete('/{news_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_authors_content(db: DB_DEPENDENCY, user: USER_DEPENDENCY,
                                   news_id: Annotated[int, Path(ge=1)]):
    if not user or user.get('role') != 'author':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    content_model = db.query(News).filter(News.id == news_id).filter(News.owner_id == user.get('id')).first()
    if not content_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Content not found')
    db.delete(content_model)
    db.commit()


@author_router.get('/get-mynews', status_code=status.HTTP_200_OK)
async def get_authors_all_news(db: DB_DEPENDENCY, user: USER_DEPENDENCY):
    if not user or user.get('role') != 'author':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    content_model = db.query(News).filter(News.owner_id == user.get('id')).all()
    if not content_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Content not found')
    return content_model

@author_router.get('/get-mynews/{news_id}', status_code=status.HTTP_200_OK)
async def get_authors_all_news(db: DB_DEPENDENCY, user: USER_DEPENDENCY, news_id: Annotated[int, Path(ge=1)]):
    if not user or user.get('role') != 'author':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    content_model = db.query(News).filter(News.id == news_id).filter(News.owner_id == user.get('id')).first()
    if not content_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Content not found')
    return content_model