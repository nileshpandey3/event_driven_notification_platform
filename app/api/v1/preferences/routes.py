"""
This is the API layer, connects HTTP requests → service/repository → DB
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.preferences.schemas import (
    PreferencesCreate,
    PreferencesResponse,
    PreferencesUpdate,
)
from app.api.v1.preferences.service import (
    add_user_preference,
    get_user_preferences,
    update_user_preference,
    remove_user_preference,
)
from app.core.auth import get_current_user
from db.session import get_db
from models import Users

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.post(
    "/",
    response_model=PreferencesResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_preferences(
    body: PreferencesCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create new preferences record for a user
    """
    user_id = user.user_id
    return add_user_preference(user_id, body, db)


@router.patch(
    "/{preference_type}",
    response_model=PreferencesUpdate,
    status_code=status.HTTP_200_OK,
)
def update_preferences(
    preference_type: str,
    body: PreferencesUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update preferences for a user
    """
    user_id = user.user_id
    return update_user_preference(
        user_id,
        preference_type,
        body,
        db,
    )


@router.get(
    "/", response_model=list[PreferencesResponse], status_code=status.HTTP_200_OK
)
def get_preferences(
    user: Users = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return all preferences for the authenticated user.
    """
    user_id = user.user_id
    return get_user_preferences(user_id, db)


@router.delete("/{preference_type}", status_code=status.HTTP_204_NO_CONTENT)
def remove_preferences(
    preference_type: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a preference for a user
    """
    user_id = user.user_id
    return remove_user_preference(user_id, preference_type, db)
