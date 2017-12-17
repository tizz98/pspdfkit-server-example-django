from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView, View

from pspdfkit_example.documents import models
from pspdfkit_example.documents.forms import UploadDocumentForm


class DocumentListView(FormView):
    form_class = UploadDocumentForm
    template_name = 'documents/index.html'

    def form_valid(self, form):
        self.user_document = form.save(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('document_detail', kwargs={
            'document_id': self.user_document.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'documents': models.UserDocument.objects.filter(
                user=self.request.user,
            ),
        })
        return context


class DocumentDetailView(TemplateView):
    template_name = 'documents/show.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.user_document = models.UserDocument.objects.get(
                id=kwargs['document_id'],
                user=self.request.user,
            )
        except models.UserDocument.DoesNotExist:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user_document.document.delete()
        return redirect('documents_list')

    def get_context_data(self, **kwargs):
        return {
            'user_document': self.user_document,
            'document': self.user_document.document,
            'instant_enabled': self.request.GET.get('instant') == 'true',
            'pspdfkit_external_url': settings.PSPDFKIT_EXTERNAL_SERVER,
            'users': User.objects.filter(is_active=True),
        }


class ShareDocumentView(View):
    def post(self, request, *args, **kwargs):
        user_ids = self.request.POST.getlist('users[]')
        user_document = models.UserDocument.objects.get(
            pk=kwargs['document_id'],
        )

        models.UserDocument.objects.filter(
            document=user_document.document,
        ).exclude(
            id=user_document.id,
        ).exclude(
            user=user_document.document.owner,
        ).delete()

        models.UserDocument.objects.bulk_create([
            models.UserDocument(
                user_id=user_id,
                document=user_document.document,
            )
            for user_id in user_ids
        ])

        return redirect(reverse('document_detail', kwargs={
            'document_id': kwargs['document_id'],
        }))
