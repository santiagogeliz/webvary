from datospaginas import choices
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.files.images import get_image_dimensions


class PortadaPrincipal(models.Model):
    imagen_banner = models.ImageField(
        blank=False,
        upload_to = 'media',
        verbose_name=u'Imagen de Fondo',
        help_text="Imagen 1920x470, tamaño máximo de 1MB"
    )
    titulo = models.CharField(
        blank=False,
        max_length=200,
        verbose_name=u'Título'
    )
    altura_titulo = models.IntegerField(
        blank=False,
        default=150,
        verbose_name=u'Altura Título',
        help_text="Este valor le dará la posición vertical al título"
    )
    subtitulo = models.CharField(
        blank=False,
        max_length=200,
        verbose_name=u'Subtítulo'
    )
    altura_subtitulo = models.IntegerField(
        blank=False,
        default=190,
        verbose_name=u'Altura Subtítulo',
        help_text="Este valor le dará la posición vertical al subtítulo"
    )
    parrafo = models.TextField(
        blank=False,
        verbose_name=u'Párrafo',
        help_text="Presiona ENTER para hacer saltos de línea"
    )
    altura_parrafo = models.IntegerField(
        blank=False,
        default=230,
        verbose_name=u'Altura Párrafo',
        help_text="Este valor le dará la posición vertical al párrafo"
    )
    color_texto = models.CharField(
        max_length=4,
        choices=choices.COLORES,
        verbose_name=u'Color del Texto',
        help_text="Seleccione un color"
    )
    imagen_segundaria = models.ImageField(
        blank=True,
        upload_to = 'media',
        verbose_name=u'Imagen Segundaria',
        help_text="Imagen 424x640, tamaño máximo de 500KB *Opcional"
    )
    altura_imagen_segundaria = models.IntegerField(
        blank=True,
        default=31,
        verbose_name=u'Altura Imagen Segundaria',
        help_text="Este valor le dará la posición vertical a la imagen"
    )
    posicion_imagen_segundaria = models.IntegerField(
        blank=True,
        default=630,
        verbose_name=u'Distancia Imagen Segundaria',
        help_text="Este valor le dará la posición horizontal a la imagen"
    )

    def clean(self):
        pk_actual = self.pk
        img_fondo = self.imagen_banner
        img_segundaria = self.imagen_segundaria
        portadas = PortadaPrincipal.objects.all()
        portadas_totales = portadas.count()
        if portadas_totales == 3 and pk_actual != portadas[0].pk and pk_actual != portadas[1].pk and pk_actual != portadas[2].pk:
            raise ValidationError("Solo puede crear un máximo de 3 Portadas Principales.")
        if img_fondo:
            w, h = get_image_dimensions(img_fondo)
            if w != 1920:
                raise ValidationError("El ancho para 'Imagen de Fondo' debe ser de %spx. El archivo seleccionado tiene %spx" %(1920, w))
            if h != 470:
                raise ValidationError("El alto para 'Imagen de Fondo' debe ser de %spx. El archivo seleccionado tiene %spx" %(470, h))
            filesize = img_fondo.size
            if filesize > 1000*1024:
                raise ValidationError("El tamaño máximo para 'Imagen de Fondo' es de %sKB" %(1000))
        if img_segundaria:
            w, h = get_image_dimensions(img_segundaria)
            if w > 424:
                raise ValidationError("El ancho máximo para 'Imagen Segundaria' es de %spx. El archivo seleccionado tiene %spx" %(424, w))
            if h > 640:
                raise ValidationError("El alto máximo para 'Imagen Segundaria' es de %spx. El archivo seleccionado tiene %spx" %(640, h))
            filesize = img_segundaria.size
            if filesize > 500*1024:
                raise ValidationError("El tamaño máximo para 'Imagen Segundaria' es de %sKB" %(500))
    
    class Meta:
        verbose_name = "Portada Principal"
        verbose_name_plural = 'Portadas Principales'

    def __str__(self):
        return u'%s' % (self.titulo)



class ProductoDestacado(models.Model):
    imagen_producto = models.ImageField(
        upload_to = 'media',
        verbose_name=u'Imagen del Producto',
        help_text="Imagen 573x394, tamaño máximo de 350KB"
    )
    titulo = models.CharField(
        blank=False,
        max_length=200,
        verbose_name=u'Título'
    )
    subtitulo = models.CharField(
        blank=False,
        max_length=200,
        verbose_name=u'Subtítulo'
    )
    link = models.ForeignKey(
    	CategoriaProducto,
    	on_delete=models.CASCADE,
    	blank=False,
        verbose_name=u'Link del botón',
        help_text="Seleccione una Categoria"
    )

    def clean(self):
        pk_actual = self.pk
        img_product = self.imagen_producto
        productos = ProductoDestacado.objects.all()
        productos_totales = productos.count()
        if productos_totales == 4 and pk_actual != productos[0].pk and pk_actual != productos[1].pk and pk_actual != productos[2].pk and pk_actual != productos[3].pk:
            raise ValidationError("Solo puede crear un máximo de 4 Productos Destacados.")
        if img_product:
            w, h = get_image_dimensions(img_product)
            if w != 573:
                raise ValidationError("El ancho para 'Imagen del Producto' debe ser de %spx. El archivo seleccionado tiene %spx" %(573, w))
            if h != 394:
                raise ValidationError("El alto para 'Imagen del Producto' debe ser de %spx. El archivo seleccionado tiene %spx" %(470, h))
            filesize = img_product.size
            if filesize > 350*1024:
                raise ValidationError("El tamaño máximo para 'Imagen del Producto' es de %sKB" %(350))
    
    class Meta:
        verbose_name = "Producto Destacado"
        verbose_name_plural = 'Productos Destacados'

    def __str__(self):
        return u'%s' % (self.titulo)



class InfoEmpresa(models.Model):
	titulo_nosotros = models.CharField(
		blank=False,
		verbose_name=u'Título de Sección',
		help_text='Tírulo que aparecerá en la sección Nosotros'
	)
	parrafo_uno = models.TextField(
		blank=False,
		verbose_name=u'Primer Párrafo',
		help_text='Primer párrafo que aparecerá en la sección Nosotros'
	)
	parrafo_dos = models.TextField(
		blank=True,
		verbose_name=u'Segundo Párrafo',
		help_text='Segundo párrafo que aparecerá en la sección Nosotros'
	)
	parrafo_tres = models.TextField(
		blank=True,
		verbose_name=u'Tercer Párrafo',
		help_text='Tercer párrafo que aparecerá en la sección Nosotros'
	)
	imagen_nosotros = models.ImageField(
		blank=False,
		upload_to='media',
		verbose_name=u'Imagen de Sección',
		help_text='Imagen 1920x470, tamaño máximo de 1MB'
	)

	def clean(self):
		pk_actual = self.pk
		imagen = self.imagen_nosotros
		nosotros = Nosotros.objects.all()
		total_nosotros = nosotros.count()
		if total_nosotros == 1 and pk_actual != total_nosotros[0].pk:
			raise ValidationError("Solo se puede crear una unica sección 'Nosotros'.")
		if imagen:
			w, h = get_image_dimensions(imagen)
            if w != 1920:
                raise ValidationError("El ancho para 'Imagen de Sección' debe ser de %spx. El archivo seleccionado tiene %spx" %(1920, w))
            if h != 470:
                raise ValidationError("El alto para 'Imagen de Sección' debe ser de %spx. El archivo seleccionado tiene %spx" %(470, h))
            filesize = imagen.size
            if filesize > 1000*1024:
                raise ValidationError("El tamaño máximo para 'Imagen de Sección' es de %sKB" %(1000))

    class Meta:
        verbose_name = "Sección Nosotros"
        verbose_name_plural = 'Sección Nosotros'

    def __str__(self):
        return u'%s' % (self.titulo_nosotros)



class Contacto(models.Model):
    descripcion_derecha = models.TextField(
        blank=False,
        verbose_name=u'Descripción Columna Derecha',
        help_text='Descripción que aparecerá en la sección de contacto'
    )
    descripcion_pie = models.TextField(
        blank=False,
        verbose_name=u'Descripción Pie de Página',
        help_text='Descripción que aparecerá en el pie de página del sitio web'
    )
    ubicacion = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=u'Ubicación',
        help_text='Escribe una ciudad y país'
    )
    telefono = models.CharField(blank=True, max_length=50)
    email = models.EmailField(blank=False, max_length=200)
    sitio_web = models.CharField(blank=True, max_length=50)
    facebook = models.URLField(
        blank=True,
        help_text='Escribe el enlace hacia tu página de Facebook'
    )
    instagram = models.URLField(
        blank=True,
        help_text='Escribe el enlace hacia tu página de Instagram'
    )


    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contacto"

    def __str__(self):
        return '%s %s' % (self.email, self.sitio_web)


class CategoriaProducto(models.Model):
	nombre = models.CharField(
        max_length=255,
        blank=False,
        verbose_name=u'Nombre de Categoria'
    )

    class Meta:
        verbose_name = "Categoria Producto"
        verbose_name_plural = 'Categorias Productos'

    def __str__(self):
        return u'%s' % (self.nombre)


class Producto(models.Model):
    nombre = models.CharField(
        max_length=255,
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
    	blank=False
    )
    imagen = models.ImageField(
        upload_to = 'media',
        verbose_name=u'Imagen principal',
        help_text="Esta imagen aparecerá en el perfil del producto"
    )
    descripcion = models.TextField(
        blank=False,
        verbose_name=u'Descripción',
        help_text='Escribe una breve descripción del producto'
    )
    estado_publicacion = models.CharField(
        max_length=255,
        help_text="Esta opción te permite guardar los datos en borrador sin publicarlos en la página",
        verbose_name=u'Estado del producto',
        choices=choices.ESTADOS_PUBLICACION
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return u'%s , %s' % (self.nombre, self.categoria)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Producto, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('equiposlab', kwargs = {'id':self.id})

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

