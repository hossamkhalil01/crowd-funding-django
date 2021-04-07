from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
    path('profile/', views.profile, name="user_profile"),
    path('donations/', views.donations, name="user_donations"),
    path('edit/', views.edit, name='user_edit'),
    url(r'^(?P<user_id>\d+)/delete$', views.delete, name='user_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)