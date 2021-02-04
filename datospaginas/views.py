from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.mail import EmailMessage

from .models import PortadaPrincipal, ProductoDestacado, ClienteDestacado, Nosotros, Contacto, CategoriaProducto, Producto, Servicio, CategoriaBlog, Blog
from .forms import ContactoForm

def home(request):
    servicios = Servicio.objects.all()
    productos = Producto.objects.all()
    post = Blog.objects.filter(estado_publicacion='Publicado')
    categorias = CategoriaProducto.objects.all()
    info_contacto = Contacto.objects.all().last()
    nosotros = Nosotros.objects.all().last()
    clientes = ClienteDestacado.objects.all().order_by('nombre_cliente')
    productos_destacados = ProductoDestacado.objects.all().order_by('pk')
    portadas_principales = PortadaPrincipal.objects.all().order_by('primera_portada')
    paginator = Paginator(clientes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    contexto = {
        'clientes':clientes,
        'page_obj': page_obj,
        'categorias': categorias,
        'info_contacto': info_contacto,
        'nosotros': nosotros,
        'servicios': servicios,
        'productos':productos,
        'post': post,
        'productos_destacados': productos_destacados,
        'portadas_principales': portadas_principales,
    }
    return render(request, 'datospaginas/home.html', contexto)


def nosotros(request):
    servicios = Servicio.objects.all()
    productos = Producto.objects.all()
    post = Blog.objects.filter(estado_publicacion='Publicado')
    categorias = CategoriaProducto.objects.all()
    info_contacto = Contacto.objects.all().last()
    nosotros = Nosotros.objects.all().last()
    clientes = ClienteDestacado.objects.all().order_by('nombre_cliente')
    portadas_principales = PortadaPrincipal.objects.all().order_by('primera_portada')
    contexto = {
        'clientes':clientes,
        'categorias': categorias,
        'info_contacto': info_contacto,
        'nosotros': nosotros,
        'servicios': servicios,
        'productos':productos,
        'post': post,
        'portadas_principales': portadas_principales,
    }
    return render(request, 'datospaginas/nosotros.html', contexto)



def contacto(request):
    servicios = Servicio.objects.all()
    productos = Producto.objects.all()
    post = Blog.objects.filter(estado_publicacion='Publicado')
    categorias = CategoriaProducto.objects.all()
    info_contacto = Contacto.objects.all().last()
    if request.method == 'POST':
        formulario = ContactoForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['name'] 
            contenido = formulario.cleaned_data['comments'] + '\n\n\n'
            contenido += 'Enviado desde la pagina web por ' + formulario.cleaned_data['name']
            contenido += '. Correo: ' + formulario.cleaned_data['email']
            contenido += '. Telefono: ' + formulario.cleaned_data['telefono']
            # El correo desde donde se envia es el primero
            # El correo adentro de la lista [] es el que recibe
            correo = EmailMessage(nombre, contenido,'gelizsantiago93@gmail.com', ['gelizsantiago93@gmail.com'] )
            correo.send()
            return HttpResponseRedirect('/')
    else:
        formulario = ContactoForm(auto_id='%s')
    contexto = {
        'formulario': formulario,
        'categorias': categorias,
        'servicios': servicios,
        'productos':productos,
        'post': post,
        'info_contacto': info_contacto,
    }
    return render(request, 'datospaginas/contacto.html', contexto)


def categoria(request, pk):
    servicios = Servicio.objects.all()
    post = Blog.objects.filter(estado_publicacion='Publicado')
    info_contacto = Contacto.objects.all().last()
    categorias = CategoriaProducto.objects.all()
    categoria = get_object_or_404(CategoriaProducto, pk=pk)
    productos = Producto.objects.filter(categoria = categoria)
    contexto = {
        'info_contacto': info_contacto,
        'categoria': categoria,
        'categorias': categorias,
        'productos' : productos,
        'servicios': servicios,
        'post': post,
	}
    return render(request, 'datospaginas/categoria.html', contexto)

def producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    productos = Producto.objects.filter(categoria = producto.categoria)
    relacionados = productos.exclude(id=pk).order_by('?')[:3]
    categorias = CategoriaProducto.objects.all()
    categoria = categorias.get(nombre=producto.categoria)
    post = Blog.objects.filter(estado_publicacion='Publicado')
    servicios = Servicio.objects.all()
    info_contacto = Contacto.objects.all().last()
    contexto = {
        'producto': producto,
        'relacionados': relacionados,
        'categorias': categorias,
        'categoria': categoria,
        'servicios': servicios,
        'info_contacto': info_contacto,
        'post': post,
    }
    return render(request, 'datospaginas/producto.html', contexto)

def servicio(request):
    servicios = Servicio.objects.all()
    productos = Producto.objects.all()
    categorias = CategoriaProducto.objects.all()
    post = Blog.objects.filter(estado_publicacion='Publicado')
    info_contacto = Contacto.objects.all().last()
    contexto = {
        'servicios': servicios,
        'productos': productos,
        'categorias': categorias,
        'info_contacto': info_contacto,
        'post': post,
    }
    return render(request, 'datospaginas/servicio.html', contexto)

def blog(request):
    post = Blog.objects.filter(estado_publicacion='Publicado').last()
    if post:
        recents_posts = Blog.objects.filter(estado_publicacion='Publicado').exclude(id=post.pk).order_by('-fecha_creacion')[:3]
    else:
        recents_posts = None
    post_categories = CategoriaBlog.objects.all().order_by('nombre')
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()
    info_contacto = Contacto.objects.all().last()
    categorias = CategoriaProducto.objects.all()
    contexto = {
        'info_contacto': info_contacto,
        'categorias': categorias,
        'productos' : productos,
        'servicios': servicios,
        'post':post,
        'recents_posts':recents_posts,
        'post_categories':post_categories,
    }
    return render(request, 'datospaginas/blog.html', contexto)

def post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    posts = Blog.objects.filter(categoria = post.categoria, estado_publicacion='Publicado')
    relacionados = posts.exclude(id=pk).order_by('?')[:2]
    info_contacto = Contacto.objects.all().last()
    categorias = CategoriaProducto.objects.all()
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()
    contexto = {
        'info_contacto': info_contacto,
        'categorias': categorias,
        'productos' : productos,
        'servicios': servicios,
        'post':post,
        'relacionados':relacionados,
    }
    return render(request, 'datospaginas/post.html', contexto)

def post_category(request, pk):
    categori = get_object_or_404(CategoriaBlog, pk=pk)
    posts = Blog.objects.filter(categoria = categori, estado_publicacion='Publicado').order_by('-fecha_creacion')
    post_categories = CategoriaBlog.objects.all().order_by('nombre')
    info_contacto = Contacto.objects.all().last()
    categorias = CategoriaProducto.objects.all()
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    contexto = {
        'info_contacto': info_contacto,
        'categorias': categorias,
        'productos' : productos,
        'categori': categori,
        'servicios': servicios,
        'posts': posts,
        'page_obj': page_obj,
        'post_categories':post_categories,
    }
    return render(request, 'datospaginas/post_category.html', contexto)

def all_posts(request):
    posts = Blog.objects.filter(estado_publicacion='Publicado').order_by('-fecha_creacion')
    post_categories = CategoriaBlog.objects.all().order_by('nombre')
    info_contacto = Contacto.objects.all().last()
    categorias = CategoriaProducto.objects.all()
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    contexto = {
        'info_contacto': info_contacto,
        'categorias': categorias,
        'productos' : productos,
        'servicios': servicios,
        'posts':posts,
        'page_obj': page_obj,
        'post_categories':post_categories,
    }
    return render(request, 'datospaginas/all_posts.html', contexto)