
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


from apps.procesos.forms import ProcesoForm, ProductoForm
from apps.procesos.models import ClienteProveedor, Producto, Descuento, Proceso, Detalle, TipoProceso, Empleado, Inventario

# Create your views here.

@login_required
def facturaCrear(request):
	message = None
	mess_tipo = 0
	#reiniciarSecuencia('PAPELERIA_ITEMS_SQ')
	print "Se reinicio Secuencia"	
	if request.method == 'POST':
		form = ProductoForm(request.POST)
		if form.is_valid():
			form.save()
			message = 'La venta se ha realizado satisfactoriamente'
			mess_tipo = 2
		proceso = json.loads(request.POST.get('proceso'))
		if 'clienProv' in  proceso:
			if len(proceso['producto']) > 0:
				total = 0

				for k in proceso['producto']:
					descuento = descProducto(k['cantidad'])
					p = Producto.objects.get(id=k['serial']).precio			
					ganancia = Producto.objects.get(id=k['serial']).ganancia
					precio = p + (p * (float(ganancia) / 100))
					subTotal = (precio * int(k['cantidad'])) - ((precio * int(k['cantidad'])) * (float(descuento)/100))
					total += subTotal

				crearProceso = Proceso(
					tipoProceso = TipoProceso.objects.get(id=proceso['tipoPro']),
					clienteProveedor = ClienteProveedor.objects.get(id=proceso['clienProv']),
					fecha = timezone.now(),
					total_facturado = total,
					empleado = Empleado.objects.get(id=request.user.get_profile().pk)
					)
				crearProceso.save()
				print "proceso guardado"
				print crearProceso.id

				for k in proceso['producto']:
					crearDetalle = Detalle(
						item = int(k['item']),
						producto = Producto.objects.get(id=k['serial']),
						precio = p + (p * (float(ganancia) / 100)),
						cantidad = int(k['cantidad']),
						descuento = Descuento.objects.get(id=int(descProducto(k['cantidad']))),
						total = (precio * int(k['cantidad'])) - ((precio * int(k['cantidad'])) * (float(descuento)/100)),
						proceso = crearProceso
						)
					crearDetalle.save()
				print "detaller guardado"
				print "Proceso numero: " , Proceso.objects.get(id=crearProceso.id).numProceso
				
				cur = connection.cursor()
				results = cur.callproc('PROCE01', [Proceso.objects.get(id=crearProceso.id).numProceso, 'E', request.user.get_profile().pk, 0])
				cur.close()
				print results
				print "Inventario Actualizado"
				message = 'La venta se ha realizado satisfactoriamente'
				mess_tipo = 2

			else:
				message = 'No se ha seleccionado ningun producto'
				mess_tipo = 1
		else:
			message = 'El cliente no ha sido seleccionado'
			mess_tipo = 1

	else:
		form = ProductoForm()
	sqfactura = getValorSecuencia('1')
	return render_to_response('facturacion/crear_factura.html', {'message': message, 'form': form, 'mess_tipo': mess_tipo, 'sqfactura': sqfactura}, context_instance=RequestContext(request))

@login_required
def ordenCompraCrea(request):
	message = None
	mess_tipo = 0
	reiniciarSecuencia('PAPELERIA_ITEMS_SQ')
	print "Se reinicio Secuencia"	
	if request.method == 'POST':
		proceso = json.loads(request.POST.get('proceso'))
		if 'clienProv' in  proceso:
			if len(proceso['producto']) > 0:
				total = 0

				for k in proceso['producto']:
					precio = Producto.objects.get(id=k['serial']).precio
					subTotal = precio * int(k['cantidad'])
					total += subTotal

				crearProceso = Proceso(
					tipoProceso = TipoProceso.objects.get(id=proceso['tipoPro']),
					clienteProveedor = ClienteProveedor.objects.get(id=proceso['clienProv']),
					fecha = timezone.now(),
					total_facturado = total,
					empleado = Empleado.objects.get(id=request.user.get_profile().pk)
					)
				crearProceso.save()
				print "proceso guardado"
				print crearProceso.id

				for k in proceso['producto']:
					crearDetalle = Detalle(
						item = int(k['item']),
						producto = Producto.objects.get(id=k['serial']),
						precio = precio,
						cantidad = int(k['cantidad']),
						descuento = Descuento.objects.get(id=int(1)),
						total = precio * int(k['cantidad']),
						proceso = crearProceso
						)
					crearDetalle.save()
				print "detaller guardado"
				message = 'La Orden de Compra se ha realizado satisfactoriamente'
				mess_tipo = 2
			else:
				message = 'No se ha seleccionado ningun producto'
				mess_tipo = 1
		else:
			message = 'El cliente no ha sido seleccionado'
			mess_tipo = 1
	sqfactura = getValorSecuencia('2')
	return render_to_response('facturacion/crear_orden_compra.html', {'message': message, 'mess_tipo': mess_tipo, 'sqfactura': sqfactura}, context_instance=RequestContext(request))

@login_required
def remisionCompraCrea(request):
	message = None
	mess_tipo = 0	
	reiniciarSecuencia('PAPELERIA_ITEMS_SQ')
	print "Se reinicio Secuencia"	
	if request.method == 'POST':
		proceso = json.loads(request.POST.get('proceso'))
		print request.POST.get('proceso')
		if 'clienProv' in  proceso:
			if len(proceso['producto']) > 0:
				total = 0

				for k in proceso['producto']:
					precio = Producto.objects.get(id=k['serial']).precio
					subTotal = precio * int(k['cantidad'])
					total += subTotal

				crearProceso = Proceso(
					tipoProceso = TipoProceso.objects.get(id=proceso['tipoPro']),
					clienteProveedor = ClienteProveedor.objects.get(id=proceso['clienProv']),
					fecha = timezone.now(),
					total_facturado = total,
					empleado = Empleado.objects.get(id=request.user.get_profile().pk),
					remision = Proceso.objects.get(id=proceso['orden'])
					)
				crearProceso.save()
				print "proceso guardado"
				print crearProceso.id

				for k in proceso['producto']:
					crearDetalle = Detalle(
						item = int(k['item']),
						producto = Producto.objects.get(id=k['serial']),
						precio = precio,
						cantidad = int(k['cantidad']),
						descuento = Descuento.objects.get(id=int(1)),
						total = precio * int(k['cantidad']),
						proceso = crearProceso
						)
					crearDetalle.save()
				print "detaller guardado"
				print "Proceso numero: " , Proceso.objects.get(id=crearProceso.id).numProceso
				
				cur = connection.cursor()
				results = cur.callproc('PROCE01', [Proceso.objects.get(id=crearProceso.id).numProceso, 'I', request.user.get_profile().pk, 0])
				cur.close()
				print results
				print "Inventario Actualizado"
				message = 'La venta se ha realizado satisfactoriamente'
				mess_tipo = 2
			else:
				message = 'No se ha seleccionado ningun producto'
				mess_tipo = 1
		else:
			message = 'El cliente no ha sido seleccionado'
			mess_tipo = 1
	sqfactura = getValorSecuencia('3')
	return render_to_response('facturacion/crear_remision_compra.html', {'message': message, 'mess_tipo': mess_tipo, 'sqfactura': sqfactura}, context_instance=RequestContext(request))


# Busqueda de clientes para factura
def buscarCliente(request):
	idCliente  = request.GET['id']
	cliente = ClienteProveedor.objects.filter(numIdentificacion=idCliente)
	data = serializers.serialize('json', cliente, fields=('nombre', 'apellido', 'email', 'numIdentificacion'))
	return HttpResponse(data, mimetype='application/json')

# Busqueda de proveedor para factura
def buscarProveedor(request):
	idCliente  = request.GET['id']
	cliente = ClienteProveedor.objects.filter(numIdentificacion=idCliente, tipo=1)
	data = serializers.serialize('json', cliente, fields=('nombre', 'email', 'numIdentificacion'))
	return HttpResponse(data, mimetype='application/json')

# Busqueda de producto para factura
def buscarProducto(request):
	idProducto  = request.GET['id']
	producto = Producto.objects.filter(id=idProducto)
	data = serializers.serialize('json', producto, fields=('nombre', 'precio', 'id', 'ganancia'))	
	return HttpResponse(data, mimetype='application/json')

def getValorSecuencia(proceso):
	cursor = connection.cursor()
	cursor.execute("select MAX(NUM_PROCESO) + 1 from PAPELERIA_PROCESO WHERE TIPO_PROCESO = " + proceso + " order by NUM_PROCESO")
	results = cursor.fetchone()
	cursor.close()
	if results[0] is None:
		return 1
	return results[0]

def ejecutarSecuencia(request):
	cursor = connection.cursor()
	cursor.execute("SELECT PAPELERIA_ITEMS_SQ.nextval FROM dual")
	results = cursor.fetchone()
	cursor.close()
	data = json.dumps({'item': results[0]})
	return HttpResponse(data, mimetype='application/json')

def descProducto(cantidad):
	cursor = connection.cursor()
	cursor.execute("SELECT ID FROM PAPELERIA_DESCUENTO WHERE CANTIDAD_MIN <= " + cantidad + " AND CANTIDAD_MAX >= " + cantidad)
	results = cursor.fetchone()
	return results[0]

def descuentoProducto(request):
	cursor = connection.cursor()
	descuento = request.GET['descuento']
	cursor.execute("SELECT DESCUENTO FROM PAPELERIA_DESCUENTO WHERE CANTIDAD_MIN <= " + descuento + " AND CANTIDAD_MAX >= " + descuento)
	results = cursor.fetchone()
	cursor.close()
	data = json.dumps({'descuento': results[0]})
	return HttpResponse(data, mimetype='application/json')

def reiniciarSecuencia(procedimiento):
	cur = connection.cursor()
	results = cur.callproc('RESET_SEQ', [procedimiento,])		
	cur.close()
	return results

def buscarOrdenCompra(request):
	numOrden  = request.GET['numOrden']	
	data = serializers.serialize('json', Proceso.objects.all().filter(numProceso=numOrden, tipoProceso=2))
	return HttpResponse(data, mimetype='application/json')

def buscarOrdenDetalle(request):
	orden  = request.GET['ordenDetalle']	
	data = serializers.serialize('json', Detalle.objects.filter(proceso=orden))
	return HttpResponse(data, mimetype='application/json')

def consultarIntentario(request):
	datos = Inventario.objects.all()
	# select P.NOMBRE, P.PRECIO, I.SALDO, S.NOMBRE from PAPELERIA_INVENTARIO I, PAPELERIA_PRODUCTO P, PAPELERIA_SEDE S WHERE I.PRODUCTO = P.ID AND I.SEDE = S.ID")
	return render_to_response('inventario/consultar_inventario.html', {'datos': datos}, context_instance=RequestContext(request))

def productoCrear(request):
	if request.method == 'POST':
		form = ProductoForm(request.POST)
		if form.is_valid():
			
			print 'Creando Producto'
		form.save()
	else:
		form = ProductoForm()
	return render_to_response('producto/crear_producto.html', {'form': form}, context_instance=RequestContext(request))
	
	

	