from fastapi import FastAPI
from app.database.database import engine,Base
from app.routes.auth_routes import auth_router
from app.routes.task_routes import task_router
from fastapi.middleware.cors import CORSMiddleware

# XP Practice : Bind Database Table schemas immediately on runtime initialization
Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Task Manager Full Stack Application")

# connect our decoupled auth routing slice and Task routing slice
app.include_router(auth_router)
app.include_router(task_router)

# Allow your local React development server
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
