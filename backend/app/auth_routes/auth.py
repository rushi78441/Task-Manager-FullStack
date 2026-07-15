from fastapi import APIRouter, Depends,HTTPException,status
from app.database.database import SessionLocal
from sqlalchemy.orm import Session
from app.schemas.auth import UserRegisterRequest,UserResponse
from app.domain.user import User
from app.security.crypto import hash_password
from app.sql_repo.user_repository import SQLUserRepository

router = APIRouter(prefix = "/auth", tags = ['Authentication'])

# Structural dependency to provision an isolated DB Session per request transaction
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register" , response_model = UserResponse , status_code = status.HTTP_201_CREATED)
def register_user(payload: UserRegisterRequest , db : Session = Depends(get_db)) -> UserResponse:
    repo = SQLUserRepository(db)

    # If user already registered (check by get email)
    if repo.get_by_email(payload.email):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "User Already Registered"
        )
    
    # Get Secured Hash Password
    secured_password = hash_password(payload.password)

    # Instantiate new User (Register it)
    new_user = User(email = payload.email , hashed_password = secured_password)

    # save via the repo interface
    saved_user = repo.save(new_user)

    return saved_user