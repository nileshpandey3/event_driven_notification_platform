from pydantic import BaseModel
from typing import Dict

class PreferencesRequest(BaseModel):
    default_channel: Dict[str, bool]
    notification_type: Dict[str, bool]
    mandatory: bool


class PreferencesResponse(PreferencesRequest):
    user_id: str
