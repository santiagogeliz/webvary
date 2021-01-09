from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from productos.models import PortadaPrincipal,ProductoDestacado,InfoEmpresa,Contacto,CategoriaProducto,Producto


User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    # form = UserChangeForm
    # add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "email", "is_superuser"]
    search_fields = ["name"]


class ContactoAdmin(admin.ModelAdmin):
    list_display = (
        'sitio_web',
        'ubicacion',
        'telefono',
        'email',
        'creado',
        'actualizado'
    )

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        return False

admin.site.register(Contacto, ContactoAdmin)


class InfoEmpresaAdmin(admin.ModelAdmin):
    list_display = (
        'titulo_nosotros','imagen_nosotros'
    )

admin.site.register(InfoEmpresa, InfoEmpresaAdmin)

class PortadaPrincipalAdmin(admin.ModelAdmin):
    list_display = (
        'titulo','color_texto','imagen_banner'
    )

admin.site.register(PortadaPrincipal, PortadaPrincipalAdmin)

class ProductoDestacadoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo','link','imagen_producto'
    )

admin.site.register(ProductoDestacado, ProductoDestacadoAdmin)


class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre'
    )

admin.site.register(CategoriaProducto, CategoriaProductoAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'categoria',
        'descripcion',
        'estado_publicacion',
        'creado',
        'actualizado'
    )
    list_filter = ('nombre', 'categoria', 'estado_publicacion')

admin.site.register(Producto, ProductoAdmin)