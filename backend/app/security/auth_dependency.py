from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
import jwt
from sqlalchemy.orm import Session
import uuid

from app.routes.auth_routes import get_db
from app.sql_repo.user_repository import SQLUserRepository
from app.domain.user import User
from app.security.crypto import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES


# This tells FastAPI to look for an "Authorization: Bearer <Token>" header automatically
security_scheme = HTTPBearer()

def get_current_user(
        credentials : HTTPAuthorizationCredentials = Depends(security_scheme),
        db: Session = Depends(get_db)
) -> User:
    """
    Dependency helper that intercepts incoming HTTP requests, decodes the JWT,
    verifies identity rules, and returns the current authenticated User domain entity.
    """

    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    try:
        # Decode the signature against our secret signing key
        payload = jwt.decode(token, key = SECRET_KEY , algorithms = ALGORITHM)
        email: str = payload["sub"]
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Query database storage to verify that the user is valid and active
    user_repo = SQLUserRepository(db)
    user = user_repo.get_by_email(email)

    if user is None:
        raise credentials_exception
    
    return user