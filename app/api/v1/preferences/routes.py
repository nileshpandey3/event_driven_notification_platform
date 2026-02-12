"""
This is the API layer, connects HTTP requests → service/repository → DB
"""
from fastapi import HTTPException

from fastapi import APIRouter, Depends, status

from app.api.v1.preferences.schemas import PreferencesCreate, PreferencesResponse, UserPreferencesResponse
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

    return add_user_preference(body, db)


@router.put(
    "/",
)
def update_preferences(user=Depends(get_current_user)):
    """
    TODO: Add the logic for the api
    """
    if user:
        return "Testing: Successful PUT response"
    return None


@router.get(
    "/",
    response_model=UserPreferencesResponse,
    status_code=status.HTTP_200_OK,
)
def get_preferences(
        user_id: int,
        user=Depends(get_current_user),
        db=Depends(get_db),
):
    """
    Get preferences for a user
    """
    assert user, f"User {user} a not a valid user or has not signed up for an account"

    preferences =  get_user_preferences(user_id, db)

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No user preferences found'
        )

    return preferences



@router.delete("/")
def remove_preferences(user=Depends(get_current_user)):
    """
    TODO: Add the logic for the api
    """
    if user:
        return "Testing: Successful DELETE response"
    return None
