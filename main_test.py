import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_index_route():
    response = client.get('/items/1')
    assert response.status_code == 200
    
def test_index_route_failing():
    response = client.get('/items/1000')
    assert response.json['q'] == 'a'
    assert response.status_code == 400