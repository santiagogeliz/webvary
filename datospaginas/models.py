from datospaginas import choices
from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.db.models import CharField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.files.images import get_image_dimensions


class PortadaPrincipal(models.Model):
    imagen_banner = models.ImageField(
        blank=False,
        upload_to = 'media',
        verbose_name=u'Imagen de Portada',
        help_text="Imagen 1920x470, tamaño máximo de 1MB."
    )
    titulo = models.CharField(
        blank=True,
        max_length=60,
        verbose_name=u'Título',
        help_text="Título que aparecerá en la Portada."
    )
    subtitulo = models.CharField(
        blank=True,
        max_length=60,
        verbose_name=u'Subtítulo',
        help_text="Subtítulo que aparecerá en la Portada."
    )
    parrafo = models.TextField(
        blank=True,
        max_length=300,
        verbose_name=u'Párrafo',
        help_text="Párrafo corto que aparecerá en la portada. Usa ENTER para saltos de línea."
    )
    color_texto = models.CharField(
        max_length=4,
        default="dark",
        choices=choices.COLORES,
        verbose_name=u'Color del Texto',
        help_text="Seleccione un color."
    )
    primera_portada = models.CharField(
        max_length=8,
        choices=choices.PORT_PRINCIPAL,
        default='inactive',
        verbose_name=u'Primera Portada',
        help_text="¿Usar como Primera Portada?"
    )

    def clean(self):
        pk_actual = self.pk
        first_banner = self.primera_portada
        img_fondo = self.imagen_banner
        portadas = PortadaPrincipal.objects.all()
        portadas_totales = portadas.count()
        primeras = PortadaPrincipal.objects.filter(primera_portada='active')
        portada_inicial = primeras.first()
        if portadas_totales == 5 and pk_actual != portadas[0].pk and pk_actual != portadas[1].pk and pk_actual != portadas[2].pk and pk_actual != portadas[3].pk and pk_actual != portadas[4].pk:
            raise ValidationError("Solo puede crear un máximo de 5 Portadas.")
        if portadas_totales == 0:
            self.primera_portada = "active"
        elif portada_inicial != None:
            if first_banner == 'active' and pk_actual != portada_inicial.pk:
                portada_inicial.primera_portada = "inactive"
                portada_inicial.save()
            elif first_banner == 'inactive' and pk_actual == portada_inicial.pk:
                raise ValidationError("Debe seleccionar una primera portada.")
        if img_fondo:
            w, h = get_image_dimensions(img_fondo)
            if w != 1920:
                raise ValidationError("El ancho para 'Imagen de Portada' debe ser de %spx. El archivo seleccionado tiene %spx." %(1920, w))
            if h != 470:
                raise ValidationError("El alto para 'Imagen de Portada' debe ser de %spx. El archivo seleccionado tiene %spx." %(470, h))
            filesize = img_fondo.size
            if filesize > 1000*1024:
                raise ValidationError("El tamaño máximo para 'Imagen de Portada' es de %sKB." %(1000))
    
    class Meta:
        verbose_name = "Portada del Sitio Web"
        verbose_name_plural = 'Portadas del Sitio Web'

    def __str__(self):
        return u'%s' % (self.titulo)




class Nosotros(models.Model):
    titulo_nosotros = models.CharField(
        max_length=60,
        blank=False,
        verbose_name=u'Título de Sección',
        help_text='Título que aparecerá en la sección Nosotros.'
    )
    introduccion = models.TextField(
        blank=False,
        verbose_name=u'Breve Introducción',
        help_text='Escribe una breve introducción sobre tu empresa. Este será el primer párrafo de la sección.'
    )
    parrafo_dos = models.TextField(
        blank=True,
        verbose_name=u'Párrafo Principal',
        help_text='Describe tu empresa más a detalle. Este será el texto principal de la sección.'
    )
    imagen_nosotros = models.ImageField(
        blank=False,
        upload_to='media',
        verbose_name=u'Imagen de Sección',
        help_text='Imagen 530x350, tamaño máximo de 1MB.'
    )

    def clean(self):
        pk_actual = self.pk
        imagen = self.imagen_nosotros
        nosotros = Nosotros.objects.all()
        total_nosotros = nosotros.count()
        if total_nosotros == 1 and pk_actual != nosotros[0].pk:
            raise ValidationError("Solo se puede crear una sección 'Nosotros'")
        if imagen:
            w, h = get_image_dimensions(imagen)
            if w != 530:
                raise ValidationError("El ancho para 'Imagen de Sección' debe ser de %spx. El archivo seleccionado tiene %spx." %(530, w))
            if h != 350:
                raise ValidationError("El alto para 'Imagen de Sección' debe ser de %spx. El archivo seleccionado tiene %spx." %(350, h))
            filesize = imagen.size
            if filesize > 1000*1024:
                raise ValidationError("El tamaño máximo para 'Imagen de Sección' es de %sKB." %(1000))

    class Meta:
        verbose_name = "Sección Nosotros"
        verbose_name_plural = 'Sección Nosotros'

    def __str__(self):
        return u'%s' % (self.titulo_nosotros)



class Contacto(models.Model):
    descripcion_derecha = models.TextField(
        blank=False,
        max_length=300,
        verbose_name=u'Texto Columna Derecha',
        help_text='Texto que aparecerá en la sección Contáctanos.'
    )
    descripcion_pie = models.TextField(
        blank=False,
        max_length=300,
        verbose_name=u'Texto Pie de Página',
        help_text='Texto que aparecerá en el pie de página del sitio web.'
    )
    logo_empresa = models.ImageField(
        blank=True,
        upload_to='media',
        verbose_name=u'Logo de la empresa',
        help_text='Imagen 250x60, tamaño máximo de 350KB.'
    )
    ubicacion = models.CharField(
        blank=False,
        max_length=100,
        verbose_name=u'Ubicación',
        help_text='Escribe la ciudad y el país donde se ubica tu empresa.'
    )
    telefono = models.CharField(blank=False, max_length=50)
    email = models.EmailField(blank=False, max_length=200)
    sitio_web = models.CharField(
        max_length=100,
        blank=True, 
        help_text='Escribe la URL de un sitio web.'
    )
    facebook = models.URLField(
        blank=True,
        help_text='Escribe la URL de tu página de Facebook.'
    )
    instagram = models.URLField(
        blank=True,
        help_text='Escribe la URL de tu página de Instagram.'
    )

    def clean(self):
        pk_actual = self.pk
        logo = self.logo_empresa
        contactos = Contacto.objects.all()
        contactos_totales = contactos.count()
        if contactos_totales == 1 and pk_actual != contactos[0].pk:
            raise ValidationError("Solo puede haber un solo registro de información de contacto.")
        if logo:
            w, h = get_image_dimensions(logo)
            if w != 250:
                raise ValidationError("El ancho para 'Logo de la empresa' debe ser de %spx. El archivo seleccionado tiene %spx." %(250, w))
            if h != 60:
                raise ValidationError("El alto para 'Logo de la empresa' debe ser de %spx. El archivo seleccionado tiene %spx." %(60, h))
            filesize = logo.size
            if filesize > 350*1024:
                raise ValidationError("El tamaño máximo para 'Logo de la empresa' es de %sKB." %(350))

    class Meta:
        verbose_name = "Sección Contáctanos"
        verbose_name_plural = "Sección Contáctanos"

    def __str__(self):
        return '%s %s' % (self.email, self.ubicacion)


class CategoriaProducto(models.Model):
    nombre = models.CharField(
        max_length=40,
        blank=False,
        verbose_name=u'Nombre de Categoria'
    )

    class Meta:
        verbose_name = "Categoria para Producto"
        verbose_name_plural = 'Categorias para Productos'

    def __str__(self):
        return u'%s' % (self.nombre)


class Producto(models.Model):
    nombre = models.CharField(
        max_length=40,
        blank=False,
        verbose_name=u'Nombre del producto'
    )
    slug = models.SlugField(
        max_length=100,
        help_text='Este campo crea la URL del perfil de este producto. Cambia si el nombre del producto cambia.'
    )
    categoria = models.ForeignKey(
        CategoriaProducto,
        on_delete=models.CASCADE,
        blank=False,
        help_text="Selecciona una categoria para el producto."
    )
    imagen = models.ImageField(
        upload_to = 'media',
        blank=False,
        verbose_name=u'Imagen del producto',
        help_text="Imagen 573x380, tamaño máximo de 350KB."
    )
    descripcion = models.TextField(
        blank=False,
        verbose_name=u'Descripción',
        help_text='Escribe una descripción del producto.'
    )

    def clean(self):
        img_product = self.imagen
        if img_product:
            w, h = get_image_dimensions(img_product)
            if w != 573:
                raise ValidationError("El ancho para 'Imagen del Producto' debe ser de %spx. El archivo seleccionado tiene %spx." %(573, w))
            if h != 380:
                raise ValidationError("El alto para 'Imagen del Producto' debe ser de %spx. El archivo seleccionado tiene %spx." %(380, h))
            filesize = img_product.size
            if filesize > 350*1024:
                raise ValidationError("El tamaño máximo para 'Imagen del Producto' es de %sKB." %(350))

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return u'%s , %s' % (self.nombre, self.categoria)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Producto, self).save(*args, **kwargs)


class ProductoDestacado(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=u'Producto',
        help_text="Seleccione un Producto."
    )
    titulo = models.CharField(
        blank=False,
        max_length=40,
        verbose_name=u'Mensaje',
        help_text="Corto mensaje que aparecerá junto al Producto Destacado."
    )

    def clean(self):
        pk_actual = self.pk
        productos = ProductoDestacado.objects.all()
        productos_totales = productos.count()
        if productos_totales == 4 and pk_actual != productos[0].pk and pk_actual != productos[1].pk and pk_actual != productos[2].pk and pk_actual != productos[3].pk:
            raise ValidationError("Solo puede crear un máximo de 4 Productos Destacados.")
    
    class Meta:
        verbose_name = "Producto Destacado"
        verbose_name_plural = 'Productos Destacados'

    def __str__(self):
        return u'%s' % (self.producto.nombre)


class Servicio(models.Model):
    nombre_servicio = models.CharField(
        max_length=50,
        blank=False,
        verbose_name=u'Nombre del Servicio'
    )
    descripcion = models.TextField(
        max_length=300,
        blank=False,
        verbose_name=u'Descripción Breve',
        help_text='Escribe una breve descripción del servicio.'
    )
    descripcion_detalle = models.TextField(
        max_length=800,
        blank=True,
        verbose_name=u'Descripción Detallada',
        help_text='Describe detalladamente el servicio.'
    )
    imagen_servicio = models.ImageField(
        upload_to = 'media',
        blank=False,
        verbose_name=u'Imagen del Servicio',
        help_text="Imagen 573x380, tamaño máximo de 350KB."
    )

    def clean(self):
        img_service = self.imagen_servicio
        if img_service:
            w, h = get_image_dimensions(img_service)
            if w != 573:
                raise ValidationError("El ancho para 'Imagen del Servicio' debe ser de %spx. El archivo seleccionado tiene %spx." %(573, w))
            if h != 380:
                raise ValidationError("El alto para 'Imagen del Servicio' debe ser de %spx. El archivo seleccionado tiene %spx." %(380, h))
            filesize = img_service.size
            if filesize > 350*1024:
                raise ValidationError("El tamaño máximo para 'Imagen del Servicio' es de %sKB." %(350))

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return u'%s' % (self.nombre_servicio)


class ClienteDestacado(models.Model):
    nombre_empresa = models.CharField(
        max_length=40,
        blank=False,
        verbose_name=u'Nombre de la empresa cliente'
    )
    nombre_cliente = models.CharField(
        max_length=40,
        blank=True,
        verbose_name=u'Nombre de la persona contacto'
    )
    imagen_cliente = models.ImageField(
        upload_to = 'media',
        blank=False,
        verbose_name=u'Imagen del cliente',
        help_text="Imagen 160x150, tamaño máximo de 350KB"
    )

    def clean(self):
        pk_actual = self.pk
        img_client = self.imagen_cliente
        clientes = ClienteDestacado.objects.all()
        clientes_totales = clientes.count()
        if clientes_totales == 6 and pk_actual != clientes[0].pk and pk_actual != clientes[1].pk and pk_actual != clientes[2].pk and pk_actual != clientes[3].pk and pk_actual != clientes[4].pk and pk_actual != clientes[5].pk:
            raise ValidationError("Solo puede crear un máximo de 6 Clientes Destacados.")
        if img_client:
            w, h = get_image_dimensions(img_client)
            if w != 160:
                raise ValidationError("El ancho para 'Imagen del cliente' debe ser de %spx. El archivo seleccionado tiene %spx." %(160, w))
            if h != 150:
                raise ValidationError("El alto para 'Imagen del cliente' debe ser de %spx. El archivo seleccionado tiene %spx." %(150, h))
            filesize = img_client.size
            if filesize > 350*1024:
                raise ValidationError("El tamaño máximo para 'Imagen del cliente' es de %sKB." %(350))

    class Meta:
        verbose_name = "Cliente Destacado"
        verbose_name_plural = 'Clientes Destacados'

    def __str__(self):
        return u'%s' % (self.nombre_empresa)


class CategoriaBlog(models.Model):
    nombre = models.CharField(
        max_length=50,
        blank=False,
        verbose_name=u'Nombre de Categoria'
    )
    imagen_categoria = models.ImageField(
        upload_to = 'media',
        blank=False,
        verbose_name=u'Imagen de Categoria',
        help_text="Imagen 573x380, tamaño máximo de 350KB"
    )

    def clean(self):
        img_categori = self.imagen_categoria
        if img_categori:
            w, h = get_image_dimensions(img_categori)
            if w != 573:
                raise ValidationError("El ancho para 'Imagen de Categoria' debe ser de %spx. El archivo seleccionado tiene %spx." %(573, w))
            if h != 380:
                raise ValidationError("El alto para 'Imagen de Categoria' debe ser de %spx. El archivo seleccionado tiene %spx." %(380, h))
            filesize = img_categori.size
            if filesize > 350*1024:
                raise ValidationError("El tamaño máximo para 'Imagen de Categoria' es de %sKB" %(350))

    class Meta:
        verbose_name = "Categoria para Artículo"
        verbose_name_plural = 'Categorias para Artículos'

    def __str__(self):
        return u'%s' % (self.nombre)


class Blog(models.Model):
    autor = models.CharField(
        max_length=50,
        blank=False,
        verbose_name=u'Autor'
    )
    titulo = models.CharField(
        max_length=60,
        blank=False,
        verbose_name=u'Título'
    )
    introduccion = models.TextField(
        blank=False,
        verbose_name=u'Breve Introducción',
        help_text='Este será el primer párrafo de tu artículo.'
    )
    contenido = RichTextField(
        blank=False,
        verbose_name=u'Contenido del Artículo',
        help_text='Escribe el texto principal de tu artículo.'
    )
    imagen_post = models.ImageField(
        upload_to = 'media',
        verbose_name=u'Imagen del Artículo',
        help_text="Imagen 940x620, tamaño máximo de 1MB."
    )
    categoria = models.ForeignKey(
        CategoriaBlog,
        on_delete=models.CASCADE,
        blank=False,
        help_text="Selecciona una categoria para el artículo."
    )
    fecha_creacion = models.DateTimeField(
        blank=True,
        default=timezone.now,
        verbose_name=u'Fecha de creación'
    )
    estado_publicacion = models.CharField(
        max_length=10,
        help_text="Esta opción te permite guardar los datos en borrador sin publicarlos en el sitio web.",
        verbose_name=u'Estado del artículo',
        choices=choices.ESTADOS_PUBLICACION
    )

    def clean(self):
        img_post = self.imagen_post
        if img_post:
            w, h = get_image_dimensions(img_post)
            if w != 940:
                raise ValidationError("El ancho para 'Imagen del Artículo' debe ser de %spx. El archivo seleccionado tiene %spx." %(940, w))
            if h != 620:
                raise ValidationError("El alto para 'Imagen del Artículo' debe ser de %spx. El archivo seleccionado tiene %spx." %(620, h))
            filesize = img_post.size
            if filesize > 1000*1024:
                raise ValidationError("El tamaño máximo para 'Imagen del Artículo' es de %sKB." %(1000))

    class Meta:
        verbose_name = "Artículo del Blog"
        verbose_name_plural = 'Artículos del Blog'

    def __str__(self):
        return u'%s' % (self.titulo)
