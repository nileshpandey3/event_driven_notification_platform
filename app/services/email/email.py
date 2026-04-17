"""
Service to send email notifications
"""

import resend

from app.core.config import RESEND_API_KEY

resend.api_key = RESEND_API_KEY


def send_email(to: str, subject: str, html: str):
    """
    Send en email notification to the desired user
    """
    params: resend.Emails.SendParams = {
        "from": "Acme Test Corp <onboarding@resend.dev>",
        "to": to,
        "subject": subject,
        "html": html,
    }

    resend.Emails.send(params)
