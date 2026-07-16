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

@task_router.post("", response_model = TaskResponse , status_code = status.HTTP_201_CREATED)
def create_task(
    payload : TaskCreateRequest,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    """
    Endpoint that accepts a title and optional description, ties the task to the
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