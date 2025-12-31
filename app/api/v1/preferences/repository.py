"""
Data Access Layer
Handles DB operations only
Performs insert/update logic
Abstracts DB implementation
"""


from fastapi import Depends
from app.core.tables import get_preferences_table

class PreferencesRepository:
    def __init__(self, table=Depends(get_preferences_table)):
        self.table = table

    def upsert_preferences(self, user_id: str, data: dict):
        # TODO: logic to add preferences in ddb table for users
        pass
