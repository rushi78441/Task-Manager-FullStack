from fastapi import Depends,HTTPException,APIRouter,status
from sqlalchemy.orm import Session
import uuid

from app.schemas.task import TaskResponse, TaskCreateRequest
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