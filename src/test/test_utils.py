from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from src.database.database import get_db, Base
import pytest
from src.models.news_model import News
from src.main import app
from src.auth.auth_utils import get_current_user
from fastapi.testclient import TestClient
from src.models.users_model import Users
from src.auth.auth_utils import pwd_context
from datetime import datetime, timezone


SQLALCHEMY_URL_DB = 'sqlite:///./testnewsx.db'
engine = create_engine(
    SQLALCHEMY_URL_DB,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'email': 'test@gmail.com', 'id': 1, 'role': 'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_news():
    news = News(
        title='News title',
        news_text='News text',
        category='News category',
        priority=4,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(news)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM news;'))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        email='test@gmail.com',
        hashed_password=pwd_context.hash('testpassword'),
        first_name='TestName',
        last_name='Testnov',
        role='admin',
        is_active=True,
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()

