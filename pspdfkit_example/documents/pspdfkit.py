from django.conf import settings

from pspdfkit import API


client = API(
    settings.PSPDFKIT_SERVER_HOST,
    settings.PSPDFKIT_API_AUTH_TOKEN
)
