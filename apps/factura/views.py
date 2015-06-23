from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import TemplateView
from django.core import serializers
from django.db import connection
import json
# Create your views here.
from .models import Cliente, Producto, Factura, DetalleFactura, CategoriaProducto
from django.db import transaction
from django.contrib import messages
from .forms import ClienteForm, CategoriaForm, ProductoForm

@login_required
@transaction.atomic
def facturaCrear(request):

    form = None
    if request.method == 'POST':
        sid = transaction.savepoint()
        try:
            proceso = json.loads(request.POST.get('proceso'))
            print proceso
            if 'serie' not in proceso:
                msg = 'Ingrese serie'
                raise Exception(msg)

            if 'numero' not in proceso:
                msg = 'Ingrese numero'
                raise Exception(msg)

            if 'clienProv' not in proceso:
                msg = 'El cliente no ha sido seleccionado'
                raise Exception(msg)

            if len(proceso['producto']) <= 0:
                msg = 'No se ha seleccionado ningun producto'
                raise Exception(msg)

            total = 0

            for k in proceso['producto']:
                producto = Producto.objects.get(id=k['serial'])
                subTotal = (producto.precio) * int(k['cantidad'])
                total += subTotal

            crearFactura = Factura(
                serie=proceso['serie'],
                numero=proceso['numero'],

                cliente=Cliente.objects.get(id=proceso['clienProv']),
                fecha=timezone.now(),
                total=total,
                vendedor=request.user
            )
            crearFactura.save()
            print "Factura guardado"
            print crearFactura.id
            for k in proceso['producto']:
                producto = Producto.objects.get(id=k['serial'])
                crearDetalle = DetalleFactura(
                    producto=producto,
                    descripcion=producto.nombre,
                    precio = producto.precio,
                    cantidad=int(k['cantidad']),
                    impuesto=producto.igv* int(k['cantidad']),
                    subtotal=producto.precio * int(k['cantidad']),
                    factura = crearFactura
                )
                crearDetalle.save()

            messages.success(
                request, 'La venta se ha realizado satisfactoriamente')
        except Exception, e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.error(request, e)

    return render_to_response('facturacion/crear_factura.html', {'form': form}, context_instance=RequestContext(request))

# Busqueda de clientes para factura


def buscarCliente(request):
    idCliente = request.GET['id']
    cliente = Cliente.objects.filter(ruc__contains=idCliente)
    data = serializers.serialize(
        'json', cliente, fields=('ruc', 'razon_social', 'direccion', 'telefono'))
    return HttpResponse(data, mimetype='application/json')

# Busqueda de producto para factura


def buscarProducto(request):
    idProducto = request.GET['id']
    producto = Producto.objects.filter(nombre__contains=idProducto)
    data = serializers.serialize(
        'json', producto, fields=('code','stock', 'nombre', 'precio', 'categoria', 'igv'))
    return HttpResponse(data, mimetype='application/json')


def consultarFactura(request):
    factura = None
    detalles = None
    sum_subtotal = 0
    sum_tax = 0
    if request.method == 'POST':
        serie = request.POST.get('serie')
        numero = request.POST.get('num')

        factura = Factura.objects.get(serie=serie, numero=numero)
        detalles = DetalleFactura.objects.filter(factura=factura)

        for d in detalles:

            sum_tax = sum_tax + d.impuesto
        sum_subtotal = factura.total-sum_tax

    return render_to_response('facturacion/print_factura.html',
                              {'factura': factura, 'detalles': detalles,
                                  'sum_subtotal': sum_subtotal, 'sum_tax': sum_tax},
                              context_instance=RequestContext(request))

def clientes(request):
    cliente=Cliente.objects.all()
    return render(request, 'facturacion/clientes.html',{'cliente':cliente})

def clienteAdd(request):
    if request.method=='POST':
        formulario=ClienteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/clientes')
    else:
        formulario=ClienteForm()
    return render_to_response('facturacion/clienteAdd.html',
                              {'formulario':formulario},
                              context_instance=RequestContext(request))
def clienteEdit (request, id):
        cliente_edit= Cliente.objects.get(pk=id)
        if request.method == 'POST':
            formulario = ClienteForm(request.POST, instance = cliente_edit)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect("/clientes")
        else:
            formulario = ClienteForm(instance= cliente_edit)
        return render_to_response('facturacion/clienteEdit.html',
                    {'formulario': formulario},
                    context_instance = RequestContext(request))
def clienteDelete (request, id):
    cliente_delete = get_object_or_404(Cliente, pk=id)
    cliente_delete.delete()
    return HttpResponseRedirect("/clientes")

def productos(request):
    productos=Producto.objects.all()
    return render(request, 'facturacion/productos.html',
                      {'productos':productos})

def productoAdd(request):
    if request.method=='POST':
        formulario=ProductoForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/productos')
    else:
        formulario=ProductoForm()
    return render_to_response('facturacion/productoAdd.html',
                              {'formulario':formulario},
                              context_instance=RequestContext(request))



def productoEdit (request, id):
        producto_edit= Producto.objects.get(pk=id)
        if request.method == 'POST':
            formulario = ProductoForm(request.POST, instance = producto_edit)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect("/productos")
        else:
            formulario = ProductoForm(instance= producto_edit)
        return render_to_response('facturacion/productoEdit.html',
                    {'formulario': formulario},
                    context_instance = RequestContext(request))

def productoDelete (request, id):
    producto_delete = get_object_or_404(Producto, pk=id)
    producto_delete.delete()
    return HttpResponseRedirect("/productos")


def categoriaAdd(request):
    if request.method=='POST':
        formulario=CategoriaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/categoria')
    else:
        formulario=CategoriaForm()
        return render_to_response('facturacion/categoriaAdd.html',
                                  {'formulario':formulario},
                                  context_instance=RequestContext(request))

def categoriaEdit (request, id):
        categoria_edit= CategoriaProducto.objects.get(pk=id)
        if request.method == 'POST':
            formulario = CategoriaForm(request.POST, instance = categoria_edit)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect("/categoria")
        else:
            formulario = CategoriaForm(instance= categoria_edit)
        return render_to_response('facturacion/categoriaEdit.html',
                    {'formulario': formulario},
                    context_instance = RequestContext(request))

def categoriaDelete (request, id):
    categoria_delete = get_object_or_404(CategoriaProducto, pk=id)
    categoria_delete.delete()
    return HttpResponseRedirect("/categoria")


def categoria(request):
    categoria=CategoriaProducto.objects.all()
    return render(request, 'facturacion/categoria.html',
                      {'categoria':categoria})


