"""
Module to handle user authentication for calling the protected endpoints
"""

import datetime
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.preferences.schemas import LoginRequest
from app.core.auth import create_access_token, get_current_user
from app.core.config import USERNAME, PASSWORD, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.redis_client import redis_client


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest):
    """
    Perform a simple auth flow with a pre-stored user and issue an access token
    """
    if data.username != USERNAME and data.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid Username or Password")

    payload = {
        "sub": data.username,
        "exp": datetime.datetime.utcnow()
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    user_id = payload["sub"]

    access_token = create_access_token(payload)

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
