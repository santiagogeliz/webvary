from django.urls import re_path, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	re_path(r'^$', views.home, name = 'home'),
	re_path(r'^Nosotros$', views.nosotros, name = 'nosotros'),
	re_path(r'^Servicios$', views.servicio, name = 'servicio'),
	re_path(r'^Productos/(?P<pk>\d+)$', views.categoria, name = 'categoria'),
	re_path(r'^Productos/detalle/(?P<pk>\d+)$', views.producto, name = 'producto'),
	re_path(r'^Contacto$', views.contacto, name = 'contacto'),
	re_path(r'^Blog$', views.blog, name = 'blog'),
	re_path(r'^Blog/Post/(?P<pk>\d+)$', views.post, name = 'post'),
	re_path(r'^Blog/Category/(?P<pk>\d+)$', views.post_category, name = 'post_category'),
	re_path(r'^Blog/All$', views.all_posts, name = 'all_posts'),
]