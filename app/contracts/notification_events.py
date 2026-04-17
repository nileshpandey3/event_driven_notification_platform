"""
Pydantic schema for validating kafka events
"""

from datetime import datetime
from typing import Literal, Optional, Dict, Any

from pydantic import BaseModel, ConfigDict, Field


class NotificationEvent(BaseModel):
    """
    Validation model for notification trigger event to be
    produced and consumed by kafka
    """

    event_id: str
    event_type: Literal[
        "PASSWORD_RESET", "SECURITY_ALERT", "PAYMENT_CONFIRMED", "SUBSCRIPTION_RENEWAL"
    ]
    user_id: int
    username: str
    occurred_at: datetime
    source_service: str
    schema_version: str = Field(default="1")
    payload: Optional[Dict[str, Any]] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)
