"""
This is the API layer, connects HTTP requests → service/repository → DB
"""

from fastapi import APIRouter, Depends, status

from app.api.v1.preferences.schemas import PreferencesCreate, PreferencesResponse
from app.api.v1.preferences.service import add_user_preference, get_user_preferences
from app.core.auth import get_current_user
from db.session import get_db

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.post(
    "/",
    response_model=PreferencesResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_preferences(
    body: PreferencesCreate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Create new preferences record for a user
    """

    assert user, f"User {user} a not a valid user or has not signed up for an account"
    user_id = user.user_id
    return add_user_preference(user_id,body, db)


@router.put("/")
def update_preferences(user=Depends(get_current_user)):
    """
    TODO: Add the logic for the api
    """
    if user:
        return "Testing: Successful PUT response"
    return None


@router.get("/", response_model=list[PreferencesResponse])
def get_preferences(
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Return all preferences for the authenticated user.
    """
    assert user, f"User {user} is not a valid user or has not signed up for an account"
    user_id = int(user)
    return get_user_preferences(user_id, db)


@router.delete("/")
def remove_preferences(user=Depends(get_current_user)):
    """
    TODO: Add the logic for the api
    """
    if user:
        return "Testing: Successful DELETE response"
    return None
