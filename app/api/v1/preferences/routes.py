"""
This is the API layer, connects HTTP requests → service/repository → DynamoDB
"""

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.post("/")
def create_preferences(user=Depends(get_current_user)):
    """
    TODO: Add the logic for the api
    """
    if user:
        return "Testing: Successful CREATE response"
    return None


@router.put("/")
def update_preferences(user=Depends(get_current_user)):
    """
    TODO: Add the logic for the api
    """
    if user:
        return "Testing: Successful PUT response"
    return None


@router.get("/")
def get_preferences(user=Depends(get_current_user)):
    """
    TODO: Add the logic for the api
    """
    if user:
        return "Testing: Successful GET response"
    return None


@router.delete("/")
def remove_preferences(user=Depends(get_current_user)):
    """
    TODO: Add the logic for the api
    """
    if user:
        return "Testing: Successful DELETE response"
    return None
