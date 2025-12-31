from fastapi import Depends
from app.core.auth import verify_jwt

def get_current_user(payload: dict = Depends(verify_jwt)):
    if payload["sub"]:
        return payload["sub"]
    return None
