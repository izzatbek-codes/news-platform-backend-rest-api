from fastapi import FastAPI, status
from src.database.database import engine, Base
from src.models import users_model, news_model
from src.auth.auth import auth_router
from src.routers.news import news_router
from src.routers.authors_news import author_router
from src.routers.admin import admin_router
from src.routers.profile import profile_router


app = FastAPI(title='NewSX')

users_model.Base.metadata.create_all(bind=engine)
news_model.Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(news_router)
app.include_router(author_router)
app.include_router(admin_router)
app.include_router(profile_router)



@app.get('/', status_code=status.HTTP_200_OK)
async def home():
    return {'message': 'Welcome to NewSX'}



