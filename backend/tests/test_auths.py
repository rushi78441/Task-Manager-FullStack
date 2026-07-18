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


@pytest.mark.asyncio
async def test_should_authentic_user_and_generate_jwt_token():
    """
    Our system should accept valid login credentials, verify them,
    and return an access token alongside its schema type.
    """

    ## Arange payloads
    registration_payload = {
        "email" : "person@example.com",
        "password" : "UserPassword123!"
    }

    login_payload = {
        "email" : "person@example.com",
        "password" : "UserPassword123!"
    }


    transport = ASGITransport(app = app)
    async with AsyncClient(transport = transport , base_url = "http://test/") as ac:
        ## Pre-populate the user: --> 
        # because in testing env , each test run should be entirely isolated and self-contained    
        await ac.post("/auth/register" , json = registration_payload)


        # Act : Attempt to login
        response = await ac.post("/auth/login" , json = login_payload)

    # assert respose 
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_should_reject_invalid_password():
    """
    Security check: A wrong password must return a 401 Unauthorized error.
    """

    # arrange payload
    registration_payload = {
        "email": "login_test@example.com",
        "password": "CorrectPassword123!"
    }

    login_payload = {
        "email": "login_test@example.com",
        "password": "WrongPassword!!"
    }

    transport = ASGITransport(app = app)
    async with AsyncClient(transport = transport , base_url = "http://test/") as ac:
        # populate the user , so account exists in database
        await ac.post("/auth/register" ,json = registration_payload)
        response = await ac.post("/auth/login" , json = login_payload)

    
    ## assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
    


