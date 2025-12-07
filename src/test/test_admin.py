from src.test.test_utils import *
from fastapi import status


def override_not_admin():
    return {'email': 'notadmin@gmail.com', 'id': 1, 'role': 'user'}

def test_delete_content_by_admin(test_news):
    response = client.delete('/admin/delete-content/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(News).filter(News.id == 1).first()
    assert not model

def test_delete_content_by_admin_not_found(test_news):
    response = client.delete('/admin/delete-content/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Content not found'}

def test_delete_user_by_admin(test_user):
    response = client.delete('/admin/delete-user/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model is None

def test_delete_user_by_admin_not_found(test_user):
    response = client.delete('/admin/delete-user/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found'}



def test_delete_user_by_admin_not_authenticated(test_user):
    app.dependency_overrides[get_current_user] = override_not_admin
    response = client.delete('/admin/delete-user/1')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}
    

def test_delete_content_by_admin_not_authenticated(test_news):
    app.dependency_overrides[get_current_user] = override_not_admin
    response = client.delete('/admin/delete-content/1')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}

