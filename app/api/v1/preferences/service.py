"""
Preference handler service: auth, schema validation, and persistence.
"""

from sqlalchemy.exc import IntegrityError

from app.api.v1.preferences.schemas import PreferencesCreate, PreferencesResponse
from models.user_preferences import UserPreferences


def get_user_preferences(user_id: int, db) -> list[PreferencesResponse]:
    """
    Return all preferences for the given user_id.
    """
    rows = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).all()
    return [
        PreferencesResponse(
            preference_type=p.preference_type,
            mandatory=p.mandatory,
            default_channel=p.default_channel,
        )
        for p in rows
    ]


def add_user_preference(
    body: PreferencesCreate,
    db,
) -> PreferencesResponse:
    """
    Add a new preference for the user if it doesn't already exist.
    Uses upsert semantics: on duplicate (user_id, preference_type), no-op and return existing.
    """
    preference = UserPreferences(
        user_id=1,
        preference_type=body.preference_type,
        mandatory=body.mandatory,
        default_channel=body.default_channel,
    )
    db.add(preference)
    try:
        db.commit()
        db.refresh(preference)
    except IntegrityError:
        db.rollback()
        existing = (
            db.query(UserPreferences)
            .filter(
                UserPreferences.user_id == 1,
                UserPreferences.preference_type == body.preference_type,
            )
            .first()
        )
        if not existing:
            raise
    return PreferencesResponse(
        preference_type=preference.preference_type,
        mandatory=preference.mandatory,
        default_channel=preference.default_channel,
    )


def update_user_preference():
    """
    TODO: Add logic to handle the request and update db if existing record exists
    """
