import jwt
import time
import urllib.parse

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.db import models

from pspdfkit_example.documents.pspdfkit import client


class Document(models.Model):
    pspdfkit_id = models.TextField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.TextField()

    def delete(self, using=None, keep_parents=False):
        server_id = self.pspdfkit_id

        try:
            delete_return_value = super().delete(
                using=using,
                keep_parents=keep_parents
            )
        except:
            pass  # bubble up the exception
        else:
            # only delete if no exception
            client.delete_document(server_id)

        return delete_return_value

    @classmethod
    def create(cls, in_memory_uploaded_file: UploadedFile, user):
        uploaded = client.upload_file_from_obj(
            in_memory_uploaded_file,
            in_memory_uploaded_file.name,
        )
        document_id = uploaded['data']['document_id']
        return cls.objects.create(
            pspdfkit_id=document_id,
            owner=user,
            name=in_memory_uploaded_file.name,
        )


class UserDocument(models.Model):
    TOKEN_LIFE = 60 * 60  # 1 hour

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    @property
    def pspdfkit_id(self):
        return self.document.pspdfkit_id

    @property
    def document_title(self):
        return self.document.name

    def get_cover_url(self):
        return '{base_url}/documents/{id}/cover?{params}'.format(
            base_url=settings.PSPDFKIT_EXTERNAL_SERVER,
            id=self.pspdfkit_id,
            params=urllib.parse.urlencode({
                'jwt': self.generate_jwt(),
                'width': '360',
            }),
        )

    def generate_jwt(self):
        return jwt.encode({
            'user_id': str(self.user_id),
            'exp': int(time.time()) + self.TOKEN_LIFE,
            'permissions': [
                'read-document',
                'edit-annotations',
                'download',
                'cover-image',
            ],
            'document_id': self.pspdfkit_id,
        }, settings.PSPDFKIT_PRIVATE_KEY, 'RS256').decode('utf-8')

    @classmethod
    def upload_example_document(cls, user):
        uploaded = client.upload_file_from_path(settings.EXAMPLE_FILE_PATH)
        print(uploaded)
        document = Document.objects.create(
            owner=user,
            pspdfkit_id=uploaded['data']['document_id'],
            name='example.pdf',
        )
        return cls.objects.create(
            document=document,
            user=user,
        )
