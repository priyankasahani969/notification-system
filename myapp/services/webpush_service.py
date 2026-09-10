import json

from pywebpush import webpush, WebPushException
from django.conf import settings


def send_web_push(subscription_info, title, message):
    try:
        response = webpush(
            subscription_info=subscription_info,

            data=json.dumps({
                "title": title,
                "message": message,
            }),

            vapid_private_key=str(settings.VAPID_PRIVATE_KEY),

            vapid_claims={
                "sub": settings.VAPID_SUBJECT,
            },
        )

        return response

    except WebPushException as e:
        return None

    except Exception as e:
        return None