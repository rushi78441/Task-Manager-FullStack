from fastapi import Depends,HTTPException,APIRouter,status
from sqlalchemy.orm import Session
import uuid

from app.schemas.task import TaskResponse, TaskCreateRequest, TaskStatusUpdateRequest
from app.domain.task import Task
from app.domain.user import User
from app.sql_repo.task_repository import SQLTaskRepository
from app.routes.auth_routes import get_db 
from app.security.auth_dependency import get_current_user

task_router = APIRouter(prefix = "/tasks" , tags = ['Tasks'])

## Task Creation route
@task_router.post("", response_model = TaskResponse , status_code = status.HTTP_201_CREATED)
def create_task(
    payload : TaskCreateRequest,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    """
    Endpoint that accepts a title and optional descryption, ties the task to the
    decoded user profile, and persists it.
    """

    ## Creating new Task
    new_task = Task(
        task_title = payload.task_title,
        descryption = payload.descryption,
        user_id = current_user.id
    )

    ## save the domain entity to our storage eng9ine via repository pattern
    repo = SQLTaskRepository(db)
    saved_task = repo.save(new_task)

    return saved_task


## Task Revrival/Fetch route
@task_router.get("", response_model = list[TaskResponse])
def fetch_user_task(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint that fetches all tasks assigned specifically to the logged-in user.
    """

    repo = SQLTaskRepository(db)
    user_tasks = repo.get_by_user(user_id = current_user.id)

    return user_tasks


## Task Status Toggle Route
@task_router.patch("/{task_id}" , response_model = TaskResponse)
def toggle_task_status(
    task_id : uuid.UUID,
    payload : TaskStatusUpdateRequest,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    
    """
    Updates the execution status of a specific task using rich domain actions.
    """
    repo = SQLTaskRepository(db)

    # Fetch the task to update 
    task = repo.get_by_id(task_id)

    # if task not found
    if not task:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Task Not Found"
        )
    
    # Security guardrails
    # If task user_id is not matched with current user Id
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not Authorized to modify this task"
        )
    
    ## Now toggle logic
    if payload.status == "completed":
        task.complete()
    elif payload.status == "active":
        task.activate()
    else:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid status transition Request"
        )
    
    ## save updated task 
    updated_task = repo.save(task)
    return updated_task


## Task Deletion Route
@task_router.delete("/{task_id}")
def delete_task(
    task_id : uuid.UUID,
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    """
    Delete the task by Task Id.
    """
    repo = SQLTaskRepository(db)

    ## Fetch the task to delete
    task = repo.get_by_id(task_id)
    # if task not found
    if not task:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Task not found"
        )
    
    ## Authorization Guard : authenticated user only delete his own task , not others
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to delete this task"
        ) 
    
    ## Deletion of task from db
    repo.delete(task_id)

    return {"message" : "Task Deleted successfully"}