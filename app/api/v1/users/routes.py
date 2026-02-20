"""
This is the API layer, connects HTTP requests → service/repository → DB
"""

from boto3 import Session
from fastapi import APIRouter, Depends, status

from app.api.v1.users.schema import UsersCreate, UsersResponse
from app.api.v1.users.service import add_user
from app.core.auth import get_current_user
from db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UsersResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    body: UsersCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new user record for a valid user
    """
    assert user, f"User {user} a not a valid user or has not signed up for an account"
    return add_user(body, db)
