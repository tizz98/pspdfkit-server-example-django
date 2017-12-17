"""pspdfkit_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from pspdfkit_example import views
from pspdfkit_example.documents import views as doc_views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('documents/',
         login_required(doc_views.DocumentListView.as_view()),
         name='documents_list'),
    path('documents/<int:document_id>/',
         login_required(doc_views.DocumentDetailView.as_view()),
         name='document_detail'),
    path('documents/<int:document_id>/share/',
         login_required(doc_views.ShareDocumentView.as_view()),
         name='share_document'),
    path('logout/', LogoutView.as_view(), name='logout'),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT,
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
