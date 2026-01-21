"""
TODO: Write Preference handler service to perform:
Auth
Schema validation
Idempotency
"""
from sqlalchemy.orm import Session
from app.models.user_preference import UserPreference
from app.preferences.schemas import PreferenceCreate

def create_or_update_preference(
    db: Session,
    user_id: str,
    payload: PreferenceCreate,
):
    pref = (
        db.query(UserPreference)
        .filter(
            UserPreference.user_id == user_id,
            UserPreference.preference_type == payload.preference_type,
        )
        .first()
    )

    if pref:
        pref.mandatory = payload.mandatory
        pref.default_channel = payload.default_channel
    else:
        pref = UserPreference(
            user_id=user_id,
            preference_type=payload.preference_type,
            mandatory=payload.mandatory,
            default_channel=payload.default_channel,
        )
        db.add(pref)

    db.commit()
    db.refresh(pref)
    return pref
