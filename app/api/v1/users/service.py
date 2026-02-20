"""
Users handler service: auth, schema validation, and persistence.
"""

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
    user = Users(user_id=body.user_id)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        existing = (
            db.query(Users)
            .filter(
                Users.user_id == body.user_id,
            )
            .first()
        )
        if not existing:
            raise
    return UsersResponse(
        user_id=body.user_id,
    )
