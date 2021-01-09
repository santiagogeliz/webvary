from django.urls import re_path, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	re_path(r'^$', views.home, name = 'home'),
	re_path(r'^Nosotros$', views.nosotros, name = 'nosotros'),
	re_path(r'^Productos/(?P<pk>\d+)$', views.categoria, name = 'categoria'),
	re_path(r'^Productos/detalle/(?P<pk>\d+)$', views.producto, name = 'producto'),
	re_path(r'^Contacto$', views.contacto, name = 'contacto'),
]