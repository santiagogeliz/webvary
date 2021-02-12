from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from .models import PortadaPrincipal, ProductoDestacado, ClienteDestacado, Nosotros, Contacto, CategoriaProducto, Producto, Servicio, CategoriaBlog, Blog



class ContactoAdmin(admin.ModelAdmin):
    list_display = (
        'ubicacion',
        'telefono',
        'email',
    )

admin.site.register(Contacto, ContactoAdmin)


class NosotrosAdmin(admin.ModelAdmin):
    list_display = (
        'titulo_nosotros','imagen_nosotros'
    )

admin.site.register(Nosotros, NosotrosAdmin)

class PortadaPrincipalAdmin(admin.ModelAdmin):
    list_display = (
        'imagen_banner','color_texto','primera_portada'
    )

admin.site.register(PortadaPrincipal, PortadaPrincipalAdmin)

class ProductoDestacadoAdmin(admin.ModelAdmin):
    list_display = (
        'producto','titulo'
    )

admin.site.register(ProductoDestacado, ProductoDestacadoAdmin)

class ClienteDestacadoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_empresa','imagen_cliente'
    )

admin.site.register(ClienteDestacado, ClienteDestacadoAdmin)


class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
    )

admin.site.register(CategoriaProducto, CategoriaProductoAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'categoria',
        'imagen',
    )
    list_filter = ('nombre', 'categoria')
    prepopulated_fields = {"slug": ("nombre",)}

admin.site.register(Producto, ProductoAdmin)

class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_servicio',
        'imagen_servicio',
    )
    list_filter = ('nombre_servicio', 'imagen_servicio')

admin.site.register(Servicio, ServicioAdmin)

class CategoriaBlogAdmin(admin.ModelAdmin):
    list_display = (
        'nombre','imagen_categoria'
    )

admin.site.register(CategoriaBlog, CategoriaBlogAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'titulo','autor','fecha_creacion','estado_publicacion'
    )

admin.site.register(Blog, BlogAdmin)