import pytest
from httpx import AsyncClient , ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_should_create_successfully_for_authenticated_user():
    """
    An authenticated user providing a valid JWT token should be able
    to create a new task under their profile profile.
    """
    ## Arrang payloads
    user_payload = {
        "email" : "task_owner@example.com",
        "password"  : "SecuredPassword123!"
    }

    task_payload = {
        "task_title" : "Finish DevOps Pipeline",
        "descryption" : "Setup CI/CD workflows using github actions"
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport , base_url= "http://test/") as ac:

        # pre- populate the user
        await ac.post("/auth/register" , json = user_payload)

        # login to get active jwt token
        login_response = await ac.post("/auth/login", json = user_payload)
        access_token = login_response.json()["access_token"]

        # Construct the authenticated header
        headers = {"Authorization" : f"Bearer {access_token}"}

        # Act : Attempt to create task
        response = await ac.post("/tasks" , json = task_payload , headers = headers)

    # assert 
    assert response.status_code == 201
    data = response.json()
    assert data["task_title"] == "Finish DevOps Pipeline"
    assert data["descryption"] == "Setup CI/CD workflows using github actions"
    assert "task_id" in data
    assert "user_id" in data    ## Prove that task is anchored to our user 


