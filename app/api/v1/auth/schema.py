"""
Pydantic schema for basic request/response validations for auth operations
"""

from pydantic import BaseModel


class PasswordReset(BaseModel):
    """
    Validation model for requesting a password reset
    using a username
    """

    username: str


class PasswordResetResponse(BaseModel):
    """
    Validation model for sending a password reset
    success response
    """

    message: str
