"""
Map for all the events to easily route them to their respective handlers
"""

from app.handlers.notification_handlers.email_notifications_handler import (
    handle_password_reset,
)

EVENT_HANDLER_MAP = {
    "PASSWORD_RESET": handle_password_reset,
}
