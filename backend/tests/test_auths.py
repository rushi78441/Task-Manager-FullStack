import pytest 
from httpx import AsyncClient , ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_should_register_user_successfully():
    """
    Our system should accept a username and plain text password, 
    register the user, and return a 201 Created status.
    """

    # user payload
    user_payload = {
        "email" : "person@example.com",
        "password" : "UserPassword123!"
    }

    # Mocking auth/register api request to get response that we furthure assert in test
    # Modern HTTPX configuration for testing ASGI apps (like FastAPI)
    transport = ASGITransport(app = app)
    async with AsyncClient(transport = transport , base_url = 'http://test') as ac:
        response = await ac.post("/auth/register", json = user_payload)

    # Assert 
    assert response.status_code == 201
    data = response.json()

    assert data["email"] == "person@example.com" , "email should be exact same as user given"
    assert "id" in data
    assert "password" not in data   ## Security check : never return password 


    

