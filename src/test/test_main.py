import pytest
from fastapi.testclient import TestClient
from src.main import app
from fastapi import status

client = TestClient(app)

@pytest.mark.asyncio
async def test_main():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Welcome to NewSX'}

