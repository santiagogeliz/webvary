from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.contrib.auth import views
from django.conf import settings
from django.views import defaults as default_views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'', include('datospaginas.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

