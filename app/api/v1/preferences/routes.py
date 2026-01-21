"""
This is the API layer, connects HTTP requests → service/repository → DynamoDB
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.preferences.schemas import PreferencesResponse, PreferencesCreate
from app.api.v1.preferences.service import create_or_update_preference
from app.core.auth import get_current_user
from db.session import get_db

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.post("/",
             response_model=PreferencesResponse,
             status_code=status.HTTP_201_CREATED,
             )
def create_preferences(
        payload: PreferencesCreate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    return create_or_update_preference(
        db=db,
        user_id=user["user_id"],
        payload=payload,
    )


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
