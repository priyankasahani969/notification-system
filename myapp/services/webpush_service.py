
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

            vapid_private_key=str(
                settings.VAPID_PRIVATE_KEY
            ),

            vapid_claims={
                "sub": settings.VAPID_SUBJECT,
            },
        )

        print("WEB PUSH SUCCESS")
        print("WEB PUSH RESPONSE:", response)

        return response

    except WebPushException as e:

        print("WEB PUSH ERROR:", e)

        if e.response:
            print(
                "WEB PUSH RESPONSE STATUS:",
                e.response.status_code
            )

            print(
                "WEB PUSH RESPONSE BODY:",
                e.response.text
            )

        return None

    except Exception as e:

        print("WEB PUSH GENERAL ERROR:", e)

        return None
