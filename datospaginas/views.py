from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage

from .models import PortadaPrincipal,ProductoDestacado,InfoEmpresa,Contacto,CategoriaProducto,Producto
from .forms import ContactoForm

def home(request):
	categorias = CategoriaProducto.all()
	nosotros = InfoEmpresa.objects.all().latest('titulo_nosotros')
    productos_destacados = ProductoDestacado.objects.all().order_by('pk')
    for producto_destacado in productos_destacados:
        if producto_destacado.link == "1":
            producto_destacado.link = "/productos/equipos-y-elementos-de-laboratorio"
        elif producto_destacado.link == "2":
            producto_destacado.link = "/productos/material-didactico"
        elif producto_destacado.link == "3":
            producto_destacado.link = "/productos/bibliobancos"
        elif producto_destacado.link == "4":
            producto_destacado.link = "/productos/muebles-escolares"
        else:
            producto_destacado.link = "/productos/equipos-audiovisuales"
    portadas_principales = PortadaPrincipal.objects.all().order_by('pk')
    info_contacto = Contacto.objects.all().latest('email')
    contexto = {
    	'categorias': categorias,
    	'nosotros': nosotros,
        'info_contacto': info_contacto,
        'portadas_principales':portadas_principales,
        'productos_destacados':productos_destacados,
    }
    return render(request, 'datospaginas/home.html', contexto)


def nosotros(request):
	portadas_principales = PortadaPrincipal.objects.all().order_by('pk')
	portadastotales = portadas_principales.count()
	nosotros = InfoEmpresa.objects.all().latest('titulo_nosotros')
    info_contacto = Contacto.objects.all().latest('email')
    contexto = {
    	'portadas_principales': portadas_principales,
    	'portadastotales': portadastotales,
        'info_contacto': info_contacto,
        'nosotros': nosotros,
    }
    return render(request, 'datospaginas/nosotros.html', contexto)



def contacto(request):
    info_contacto = Contacto.objects.all().latest('email')
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
            correo = EmailMessage(nombre, contenido,'info@dazaglobal.com', ['info@dazaglobal.com'] )
            correo.send()
            return HttpResponseRedirect('/')
    else:
        formulario = ContactoForm(auto_id='%s')
    contexto = {
        'formulario': formulario,
        'info_contacto': info_contacto,
    }
    return render(request, 'datospaginas/contacto.html', contexto)


def categoria(request):
	categorias = CategoriaProducto.all()
	info_contacto = Contacto.objects.all().latest('email')
	categoria = get_object_or_404(CategoriaProducto, pk=pk)
	productos = Producto.objects.filter(categoria = categoria)
	contexto = {
		'info_contacto': info_contacto,
		'categoria': categoria,
		'productos' : productos,
	}
	return render(request, 'datospaginas/categoria.html', contexto)

def producto(request,slug,id):
    info_contacto = Contacto.objects.all().latest('email')
    producto = get_object_or_404(Producto, slug=slug, pk=id)
    relacionados = Producto.objects.exclude(id=id).order_by('?')[:3]
    contexto = {
        'info_contacto': info_contacto,
        'producto': producto,
        'relacionados': relacionados,
    }
    return render(request, 'datospaginas/producto.html', contexto)