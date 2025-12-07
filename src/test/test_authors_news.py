from src.test.test_utils import *
from fastapi import status

def override_get_current_author_user():
    return {'email': 'testn@gnmail.com', 'id': 1, 'role': 'author'}

def override_get_fake_author():
    return {'email': 'test2@gmail.com', 'id': 3, 'role': 'user'}

def test_create_content(test_news):
    app.dependency_overrides[get_current_user] = override_get_current_author_user
    request_model = {
        'title': 'Create test title',
        'news_text': 'Test news text',
        'category': 'Add category',
        'priority': 5,
        'owner_id': 1,
    }
    
    response = client.post('/authors', json=request_model)
    # assert response.status_code == status.HTTP_201_CREATED
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['id'] == 2
    db = TestingSessionLocal()
    news_model = db.query(News).filter(News.id == data['id']).first()
    assert news_model.title == data['title']
    assert news_model.news_text == data['news_text']
    assert news_model.category == data['category']
    assert news_model.priority == data['priority']
    assert news_model.owner_id == data['owner_id']

def test_create_content_not_authenticated(test_news):
    app.dependency_overrides[get_current_user] = override_get_fake_author
    request_model = {
        'title': 'Create test title',
        'news_text': 'Test news text',
        'category': 'Add category',
        'priority': 5,
        'owner_id': 1,
    }
    response = client.post('/authors', json=request_model)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}



def test_update_content(test_news):
    app.dependency_overrides[get_current_user] = override_get_current_author_user
    request_model = {
        'title': 'Update test title',
        'news_text': 'Test news text',
        'category': 'Update category',
        'priority':4,
        'owner_id': 1,
    }
    response = client.put('/authors/1/', json=request_model)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(News).filter(News.id == 1).filter(News.owner_id == 1).first()
    assert model.title == request_model.get('title')
    assert model.category == request_model.get('category')

def test_update_content_content_not_found(test_news):
    app.dependency_overrides[get_current_user] = override_get_current_author_user
    request_model = {
        'title': 'Update test title',
        'news_text': 'Test news text',
        'category': 'Update category',
        'priority':4,
        'owner_id': 1,
    }
    response = client.put('/authors/999', json=request_model)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Content not found'}

def test_update_content_content_not_authenticated(test_news):
    app.dependency_overrides[get_current_user] = override_get_fake_author

    request_model = {
        'title': 'Update test title',
        'news_text': 'Test news text',
        'category': 'Update category',
        'priority':4,
        'owner_id': 1,
    }
    response = client.put('/authors/1', json=request_model)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}

def test_delete_content(test_news):
    app.dependency_overrides[get_current_user] = override_get_current_author_user
    response = client.delete('/authors/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(News).filter(News.id == 1).filter(News.owner_id == 1).first()
    assert model is None

def test_delete_content_not_found(test_news):
    app.dependency_overrides[get_current_user] = override_get_current_author_user
    response = client.delete('/authors/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Content not found'}

def test_delete_content_not_authenticated(test_news):
    app.dependency_overrides[get_current_user] = override_get_fake_author
    response = client.delete('/authors/1')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}

def test_get_authors_all_tests(test_news):
    app.dependency_overrides[get_current_user] = override_get_current_author_user

    response = client.get('/authors/get-mynews')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()[0]
    assert data['title'] == 'News title'
    assert data['news_text'] == 'News text'
    assert data['category'] == 'News category'

def test_get_authors_all_tests_not_authenticated(test_news):
    app.dependency_overrides[get_current_user] = override_get_fake_author
    response = client.get('/authors/get-mynews')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}

def test_get_authors_news_by_id(test_news):
    app.dependency_overrides[get_current_user] = override_get_current_author_user
    response = client.get('/authors/get-mynews/1')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == 'News title'
    assert data['news_text'] == 'News text'
    assert data['category'] == 'News category'

def test_get_authors_news_by_id_not_found(test_news):
    app.dependency_overrides[get_current_user] = override_get_current_author_user
    response = client.get('/authors/get-mynews/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Content not found'}

def test_get_authors_news_by_id_not_authenticated(test_news):
    app.dependency_overrides[get_current_user] = override_get_fake_author
    response = client.get('/authors/get-mynews/1')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}
