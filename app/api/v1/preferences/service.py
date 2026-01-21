"""
TODO: Write Preference handler service to perform:
Auth
Schema validation
Idempotency
"""
from sqlalchemy.orm import Session
from app.api.v1.preferences.schemas import PreferencesCreate

def create_or_update_preference(
    db: Session,
    user_id: str,
    payload: PreferencesCreate,
):
    """
    TODO: Add logic for the handler service
    which will validate/manipulate the incoming payload data and upsert
    """
