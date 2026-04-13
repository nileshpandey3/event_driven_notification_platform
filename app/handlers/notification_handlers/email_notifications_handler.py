"""
handler for sending email notifications to users
"""

from app.services.email.email import send_email


def handle_password_reset(event):
    """
    Handler for password reset events
    """
    send_email(
        to=f"delivered+user_{event.user_id}@resend.dev",
        subject="Password Reset Email",
        html=f"<p>Reset your password. Event ID: {event.event_id}</p>",
    )
