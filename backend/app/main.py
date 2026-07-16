from fastapi import FastAPI
from app.database.database import engine,Base
from app.routes.auth_routes import auth_router
from app.routes.task_routes import task_router

# XP Practice : Bind Database Table schemas immediately on runtime initialization
Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Task Manager Full Stack Application")

# connect our decoupled auth routing slice and Task routing slice
app.include_router(auth_router)
app.include_router(task_router)
