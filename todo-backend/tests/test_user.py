# tests/test_user.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/v1/user/", json={
        "username": "testuser",
        "password": "test1234",
        # "fullname": "Test Bruger"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_user_duplicate(client):
    response = await client.post("/v1/user/", json={
        "username": "testuser",
        "password": "test1234",
        # "fullname": "Test Bruger"
    })
    assert response.status_code == 400  # eller 409 afhængigt af din validering
