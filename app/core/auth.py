"""
Create and Decode Bearer Auth Token to authenticate a user for making API requests
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.core.config import SECRET_KEY, ALGORITHMS


def create_access_token(payload: dict):
    """
    Create a temp access token for a valid user
    """
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHMS)


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Decode the access token in the request header and return the authenticated user
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMS])
        user = payload.get("sub")

        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user

    except JWTError as exc:
        raise HTTPException(
            status_code=401, detail="Token verification failed"
        ) from exc
