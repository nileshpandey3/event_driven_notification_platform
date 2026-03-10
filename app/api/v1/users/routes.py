"""
This is the API layer, connects HTTP requests → service/repository → DB
"""

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.users.schema import UsersCreate, UsersResponse
from app.api.v1.users.service import add_user
from app.core.auth import require_admin
from db.session import get_db
from models import Users

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UsersResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    body: UsersCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user record for a valid user
    e.g. when a new user signs up for a new account
    using a website or app
    """
    return add_user(body, db)


@router.delete(
    "/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)]
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user from the Users table
    Only an Admin user can perform this action
    """
    user = db.scalar(select(Users).where(Users.user_id == user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
