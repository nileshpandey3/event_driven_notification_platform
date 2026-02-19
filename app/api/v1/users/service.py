"""
Users handler service: auth, schema validation, and persistence.
"""

from alembic.util import status
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.users.schema import UsersCreate, UsersResponse
from models import Users


def add_user(
    body: UsersCreate,
    db,
) -> UsersResponse:
    """
    Add a new user to our Users table
    """
    user = Users(username=body.username, password=body.password)
    db.add(user)

    try:
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )

    return UsersResponse(
        user_id=user.user_id,
        username=user.username,
    )
