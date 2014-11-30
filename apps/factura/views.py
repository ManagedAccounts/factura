from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import TemplateView
from django.core import serializers
from django.db import connection
import json
# Create your views here.
from .models import Cliente, Producto


@login_required
def facturaCrear(request):
    message = None
    mess_tipo = 0
    sqfactura = 1
    form = None
    return render_to_response('facturacion/crear_factura.html', {'message': message, 'form': form, 'mess_tipo': mess_tipo, 'sqfactura': sqfactura}, context_instance=RequestContext(request))

# Busqueda de clientes para factura


def buscarCliente(request):
    idCliente = request.GET['id']
    cliente = Cliente.objects.filter(ruc__contains=idCliente)
    data = serializers.serialize(
        'json', cliente, fields=('ruc', 'razon_social', 'direccion', 'telefono'))
    return HttpResponse(data, mimetype='application/json')

# Busqueda de producto para factura
def buscarProducto(request):
	idProducto  = request.GET['id']
	producto = Producto.objects.filter(nombre__contains=idProducto)
	data = serializers.serialize('json', producto, fields=('code', 'nombre', 'precio', 'categoria','igv'))	
	return HttpResponse(data, mimetype='application/json')

