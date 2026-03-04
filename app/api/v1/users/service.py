"""
Users handler service: auth, schema validation, and persistence.
"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.v1.users.schema import UsersCreate, UsersResponse
from models import Users


def add_user(
    body: UsersCreate,
    db: Session,
) -> UsersResponse:
    """
    Handler to add a new user to the Users table
    """
    user = Users(username=body.username, password=body.password)
    db.add(user)

    try:
        db.commit()
        db.refresh(user)

    except IntegrityError as exc:
        db.rollback()
        # Check if username already exists
        existing = db.scalar(select(Users).where(Users.username == user.username))
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            ) from exc
        raise

    return UsersResponse(
        user_id=user.user_id,
        username=user.username,
    )
