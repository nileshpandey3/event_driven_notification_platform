"""
Module to handle user authentication for calling the protected endpoints
"""

import datetime
from datetime import timedelta

from boto3 import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.preferences.schemas import LoginRequest
from app.core.auth import create_access_token, get_current_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.redis_client import redis_client
from db.session import get_db
from models import Users

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest, db=Depends(get_db)):
    """
    Perform a simple auth flow for an existing user
    and issue an access token for api authentication
    """

    # Find user in DB
    user = db.query(Users).filter(Users.username == data.username).first()

    if not user or user.password != data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password",
        )

    payload = {
        "sub": str(user.user_id),
        "username": user.username,
        "exp": datetime.datetime.utcnow()
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    user_id = payload["sub"]

    access_token = create_access_token(payload)

    # Store token in Redis
    redis_client.set(f"user:{user_id}:access_token", access_token, ex=3600)
    return {
        "message": "Auth Login successful",
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(user_id: str = Depends(get_current_user)):
    """
    Logout and clear the client session
    """
    redis_client.delete(f"session:{user_id}")
    return {"message": "Logged out successfully"}
