import requests
from django.conf import settings


def verify_turnstile(token):
    if not token:
        return False

    data = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token,
    }

    try:
        response = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data=data,
            timeout=5
        )
        result = response.json()
        return result.get("success", False)
    except Exception:
        return False