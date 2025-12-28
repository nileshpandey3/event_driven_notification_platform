from fastapi import Depends
from app.api.v1.preferences.repository import PreferencesRepository

class PreferencesService:
    def __init__(self, repo: PreferencesRepository = Depends()):
        self.repo = repo

    async def update_preferences(self, user_id: str, data):
        # Example business rules
        if not (data.email or data.sms or data.push):
            raise ValueError("At least one channel must be enabled")

        return await self.repo.upsert_preferences(user_id, data.dict())
