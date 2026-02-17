"""
This is the API layer, connects HTTP requests → service/repository → DB
"""

from fastapi import APIRouter, Depends, status

from app.api.v1.preferences.schemas import PreferencesCreate, PreferencesResponse, PreferencesUpdate
from app.api.v1.preferences.service import add_user_preference, get_user_preferences, update_user_preferences
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

    return add_user_preference(body, db)


@router.patch(
    "/{preference_type}",
    response_model=PreferencesUpdate
)
def update_preferences(
    preference_type: str,
    body: PreferencesUpdate,
    user=Depends(get_current_user),
    db=Depends(get_db),

):
    """
    Update preferences for a user
    """
    assert user, f"User {user} a not a valid user or has not signed up for an account"
    return update_user_preferences(
        preference_type,
        body,
        db,
    )


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
