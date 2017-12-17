from django.contrib.auth.models import User

from pspdfkit_example.documents.models import UserDocument


class SimpleAuthBackend:
    def authenticate(self, username=None, password=None):
        if username:
            user = User.objects.get_or_create(
                username=username,
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )[0]

            if not UserDocument.objects.filter(user=user).exists():
                UserDocument.upload_example_document(user)

            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
