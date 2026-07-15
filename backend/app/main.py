from fastapi import FastAPI
from app.database.database import engine,Base
from app.auth_routes.auth import router as auth_router

# XP Practice : Bind Database Table schemas immediately on runtime initialization
Base.metadata.create_all(bind = engine)

app = FastAPI(title = "Task Manager Full Stack Application")

# connect our decoupled auth routing slice
app.include_router(auth_router)