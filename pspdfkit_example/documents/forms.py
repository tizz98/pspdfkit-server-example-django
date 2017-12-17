from django import forms

from pspdfkit_example.documents import models


class UploadDocumentForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={'accept': 'application/pdf'},
        ),
    )

    def save(self, user):
        document = models.Document.create(
            self.cleaned_data['file'],
            user,
        )
        return models.UserDocument.objects.create(
            document=document,
            user=user,
        )
