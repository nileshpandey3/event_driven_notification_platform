"""
Create and Decode Bearer Auth Token to authenticate a user for making API requests
"""
from alembic.util import status
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.core.config import SECRET_KEY, ALGORITHMS
from db.session import get_db
from models import Users


def create_access_token(payload: dict):
    """
    Create a temp access token for a valid user
    """
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHMS)


security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_db)
):
    """
    Decode the access token in the request header and return the authenticated user
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMS])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Search from the user in DB
        user = db.query(Users).filter(
            Users.user_id == user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )

        return user

    except JWTError as exc:
        raise HTTPException(
            status_code=401, detail="Token verification failed"
        ) from exc
