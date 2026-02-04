"""
Users handler service: auth, schema validation, and persistence.
"""

from sqlalchemy.exc import IntegrityError

from app.api.v1.users.schema import UsersCreate, UsersResponse
from models import Users


def add_user(
    body: UsersCreate,
    db,
) -> UsersResponse:
    """
    TODO
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
