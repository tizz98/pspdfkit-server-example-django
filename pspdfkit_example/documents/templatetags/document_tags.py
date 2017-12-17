from django import template

from pspdfkit_example.documents.models import UserDocument

register = template.Library()


@register.simple_tag
def user_has_access(user, document):
    return UserDocument.objects.filter(
        user=user,
        document=document,
    ).exists()
