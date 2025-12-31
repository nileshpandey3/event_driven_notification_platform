# Pydantic schema for request/response validations

from pydantic import BaseModel
from typing import Optional

class PreferencesBase(BaseModel):
    email: bool
    sms: bool
    push: bool

class PreferencesCreate(PreferencesBase):
    pass

class PreferencesUpdate(BaseModel):
    email: Optional[bool] = None
    sms: Optional[bool] = None
    push: Optional[bool] = None

class PreferencesResponse(PreferencesBase):
    user_id: str
