import pytest
from httpx import AsyncClient , ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_should_create_task_successfully_for_authenticated_user():
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
        headers = {"Authorization" : f"bearer {access_token}"}

        # Act : Attempt to create task
        response = await ac.post("/tasks" , json = task_payload , headers = headers)

    # assert 
    assert response.status_code == 201
    data = response.json()
    assert data["task_title"] == "Finish DevOps Pipeline"
    assert data["descryption"] == "Setup CI/CD workflows using github actions"
    assert "task_id" in data
    assert "user_id" in data    ## Prove that task is anchored to our user 


@pytest.mark.asyncio
async def test_should_fetch_only_tasks_belonging_to_authenticated_user():
    """
    A user should be able to list all of their active or completed tasks, 
    ensuring isolation from other users' accounts.
    """

    transpot = ASGITransport(app = app)
    async with AsyncClient(transport = transpot, base_url = "http://test/") as ac:
        
        ## Setup User A and Create Task 
        user_a = {"email" : "usera@example.com" , "password" : "password!123"}
        await ac.post("/auth/register" , json = user_a)
        login_a = await ac.post("/auth/login" , json = user_a)
        token_a = login_a.json()["access_token"]

        # Create Task A
        await ac.post("/tasks",
                json = {"task_title" : "User A Task", "descryption" : "Private to A" , "status" : "active"},
                headers = {"Authorization" : f"bearer {token_a}"}              
        )

        ## Setup User B and Create Task
        user_b = {"email" : "userb@example.com", "password" : "password!123"}
        await ac.post("/auth/register" , json = user_b)
        login_b = await ac.post("/auth/login" , json=user_b)
        token_b = login_b.json()["access_token"]

        # Create Task B
        await ac.post("/tasks",
                json = {"task_title" : "User B Task" , "descryption" : "Private to B" , "status" : "active"},
                headers = {"Authorization" : f"bearer {token_b}"}                
         )
        

        ## Act : Attempt to retrive task of User A
        response = await ac.get("/tasks" , headers = {"Authorization" : f"bearer {token_a}"})

    ## Assert : User A only see exactly 1 task and it is their own one
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["task_title"] == "User A Task"
    assert tasks[0]["descryption"] == "Private to A"


@pytest.mark.asyncio
async def test_should_toggle_task_status_successfully_for_owner():
    """
    The owner of a task should be able to update its status to 'completed'.
    """

    transport = ASGITransport(app=app)
    async with AsyncClient(transport = transport , base_url = "http://test/") as ac:
        ## Register and login user
        user = {
            "email" : "user@example.com",
            "password" : "password!123"
        }
        await ac.post("/auth/register" , json = user)

        login_user = await ac.post("/auth/login" , json = user)
        token_user = login_user.json()["access_token"]
        header = {"Authorization" : f"bearer {token_user}"}

        ## Create task (status : active) by default
        task = await ac.post("/tasks" ,
                json = {"task_title" : "TDD Task", "descryption" : "write mode code" , "status" : "active"},
                headers = header
        )
        task_id = task.json()["task_id"]

        # ACt : toggle task from active to completed -->  we will use patch rest APi
        response = await ac.patch(f"/tasks/{task_id}", json = {"status" : "completed"}, headers = header)

    # Assert 
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

@pytest.mark.asyncio
async def test_should_delete_task_successfully_by_task_owner():
    """
    The owner of a task should be able to permanently delete it,
    and subsequent fetches should return a 404.
    """

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport , base_url = "http://test/") as ac:
        # User
        user = {
            "email" : "delete@example.com",
            "password" : "password!123"
        }

        ## Register and login user
        await ac.post("/auth/register" , json = user)
        login = await ac.post("/auth/login" , json = user)
        token = login.json()["access_token"]
        headers = {"Authorization" : f"bearer {token}"}

        ## Create task 
        task = await ac.post("/tasks", 
                json = {"task_title" : "Delete My task" , "descrypion" : "Task should be deleted" , "status" : "active"},
                headers = headers
        )
        task_id = task.json()["task_id"]

        ## ACT : Delete task by task id
        delete_response = await ac.delete(f"/tasks/{task_id}", headers = headers)

        ## Verify task is gone now by fetching it
        list_response = await ac.get("/tasks" , headers=headers)

    # Assert
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task Deleted successfully"

    # The return list should be empty
    assert len(list_response.json()) == 0



