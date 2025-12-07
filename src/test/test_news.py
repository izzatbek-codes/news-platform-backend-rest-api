from src.test.test_utils import *
from fastapi import status



def test_get_all_news(test_news):
    response = client.get('/news')
    assert response.status_code == status.HTTP_200_OK
    # assert response.json() == [{
    #     'title': 'News title',
    #     'news_text': 'News text',
    #     'category': 'News category',
    #     'priority': 4,
    #     'owner_id': 1,
    # }]
    data = response.json()[0]
    assert data['title'] == 'News title'
    assert data['news_text'] == 'News text'
    assert data['category'] == "News category"
    assert data['priority'] == 4
    assert isinstance(data['id'], int)
    assert data['id'] == 1

def test_get_news(test_news):
    response = client.get('/news/1')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == 'News title'
    assert data['news_text'] == 'News text'
    assert data['category'] == 'News category'
    assert data['priority'] == 4

def test_get_news_not_found(test_news):
    response = client.get('/news/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Content not found'}

def override_get_fake_current_user():
    return None

def test_get_all_news_without_user(test_news):
    app.dependency_overrides[get_current_user] = override_get_fake_current_user
    response = client.get('/news')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': "Not authenticated"}

def test_get_news_without_user(test_news):
    app.dependency_overrides[get_current_user] = override_get_fake_current_user
    response = client.get('/news/1')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': "Not authenticated"}


