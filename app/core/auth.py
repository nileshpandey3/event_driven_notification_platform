"""
Create and Decode Bearer Auth Token to authenticate a user for making API requests
"""

from alembic.util import status
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import SECRET_KEY, ALGORITHMS
from db.session import get_db
from models import Users
from models.users import UserRoles


def create_access_token(payload: dict):
    """
    Create a temp access token for a valid user
    """
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHMS)


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Users:
    """
    Decode the access token in the request header and return the authenticated user
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMS])

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

    try:
        user_id = int(payload.get("sub"))

    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    # Search from the user in DB
    user = db.scalar(select(Users).where(Users.user_id == user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


def require_admin(user: Users = Depends(get_current_user)):
    """
    Function to validate and return an admin user
    """
    if user.role != UserRoles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    return user
