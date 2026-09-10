import requests
from django.conf import settings


def send_email_notification(to_email, subject, content):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    data = {
        "sender": {
            "email": settings.BREVO_FROM_EMAIL,
            "name": "Notification System",
        },
        "to": [
            {
                "email": to_email,
            }
        ],
        "subject": subject,
        "htmlContent": content,
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=10,
    )

    return response