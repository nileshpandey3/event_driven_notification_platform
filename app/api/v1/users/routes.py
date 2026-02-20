"""
This is the API layer, connects HTTP requests → service/repository → DB
"""

from fastapi import APIRouter, Depends, status

from app.api.v1.users.schema import UsersCreate, UsersResponse
from app.api.v1.users.service import add_user
from db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UsersResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    body: UsersCreate,
    db=Depends(get_db),
):
    """
    Create a new user record for a valid user
    e.g. when a new user signs up for a new account
    using a website or app
    """
    return add_user(body, db)
