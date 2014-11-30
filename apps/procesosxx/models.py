from django.db import models
from django.contrib.auth.models import User
from django.db import connection

# Create your models here.

class Categoria(models.Model):
	nombre = models.CharField(max_length=100, blank=False)
	def __str__(self):
		return self.nombre
	class Meta:
		db_table = 'papeleria_categoria'

	# static method to perform a fulltext search  
	@staticmethod
	def crearCategoria(search_string):
		cur = connection.cursor()
		results = cur.callproc('CREAR_CATEGORIA', [search_string,])		
		cur.close()
		return results

class Sede(models.Model):
	nombre = models.CharField(max_length=100, blank=False)
	direccion = models.CharField(max_length=100, blank=False)
	telefono = models.IntegerField(blank=False)
	def __str__(self):
		return self.nombre
	class Meta:
		db_table = 'papeleria_sede'

class TipoIdentificacion(models.Model):
	nombre = models.CharField(max_length=100, blank=False)
	def __str__(self):
		return self.nombre
	class Meta:
		db_table = 'papeleria_tipo_identificacion'

class Cargo(models.Model):
	nombre = models.CharField(max_length=100, blank=False)
	def __str__(self):
		return self.nombre
	class Meta:
		db_table = 'papeleria_cargo'

class Empleado(models.Model):
	user = models.ForeignKey(User, unique=True)
	tipoIdentificacion = models.ForeignKey('TipoIdentificacion', db_column='tipo_identificacion')
	numIdentificacion = models.IntegerField(blank=False)
	direccion = models.CharField(max_length=100, blank=False)
	telefono = models.IntegerField(blank=False)
	sede = models.ForeignKey('Sede', db_column='sede')
	cargo = models.ForeignKey('Cargo', db_column='cargo')
	def __str__(self):
		return u"%s" % (self.numIdentificacion)
	class Meta:
		db_table = 'papeleria_empleado'

class Tipo(models.Model):
	nombre = models.CharField(max_length=100, blank=False)
	def __str__(self):
		return self.nombre
	class Meta:
		db_table = 'papeleria_tipo'

class ClienteProveedor(models.Model):
	nombre = models.CharField(max_length=100, blank=False)
	apellido = models.CharField(max_length=100, blank=False)
	direccion = models.CharField(max_length=100, blank=False)
	email = models.EmailField(max_length=254)
	tipoIdentificacion = models.ForeignKey('TipoIdentificacion', db_column='tipo_identificacion')
	numIdentificacion = models.IntegerField(blank=False)
	tipo = models.ForeignKey('Tipo', db_column='tipo')
	def __str__(self):
		return self.nombre
	class Meta:
		db_table = 'papeleria_cliente_proveedor'

class Producto(models.Model):
	nombre = models.CharField(max_length=100, blank=False)
	precio = models.IntegerField(blank=False)
	clienteProveedor = models.ForeignKey('ClienteProveedor', db_column='cliente_proveedor')
	categoria = models.ForeignKey('Categoria', db_column='categoria')
	ganancia = models.IntegerField(blank=False)
	def __str__(self):
		return self.nombre
	class Meta:
		db_table = 'papeleria_producto'

class Descuento(models.Model):
	cantidadMin = models.IntegerField(blank=False, db_column='cantidad_min')
	cantidadMax = models.IntegerField(blank=False, db_column='cantidad_max')
	descuento = models.IntegerField(blank=False)
	def __str__(self):
		return u"Cantidad: %s - %s Descuento: %s" % (self.cantidadMin, self.cantidadMax, self.descuento)
	class Meta:
		db_table = 'papeleria_descuento'

class Telefono(models.Model):
	numero = models.IntegerField(primary_key=True)
	clienteProveedor = models.ForeignKey('ClienteProveedor', db_column='cliente_proveedor')
	def __str__(self):
		return self.numero
	class Meta:
		db_table = 'papeleria_telefono'

class TipoProceso(models.Model):
	nombre = models.CharField(max_length=100, blank=False)
	def __str__(self):
		return self.nombre
	class Meta:
		db_table = 'papeleria_tipo_proceso'

class Proceso(models.Model):
	numProceso = models.IntegerField(blank=False, db_column='num_proceso')
	tipoProceso = models.ForeignKey('TipoProceso', db_column='tipo_proceso')
	clienteProveedor = models.ForeignKey('ClienteProveedor', db_column='cliente_proveedor')
	fecha = models.DateTimeField(auto_now_add=True)
	total_facturado = models.FloatField(blank=False)
	empleado = models.ForeignKey('Empleado', db_column='empleado')
	remision = models.ForeignKey('Proceso', db_column='remision', blank=True, null=True)
	def __str__(self):
		return u"id: %s" % (self.id)
	class Meta:
		db_table = 'papeleria_proceso'

class Detalle(models.Model):
	item = models.SmallIntegerField(blank=False)
	producto = models.ForeignKey('Producto', db_column='producto')
	precio = models.FloatField(blank=False)
	cantidad = models.IntegerField(blank=False)
	descuento = models.ForeignKey('Descuento', db_column='descuento')
	total = models.FloatField(blank=False)
	proceso = models.ForeignKey('Proceso', db_column='proceso')
	def __str__(self):
		return u"proceso: %s" % (self.proceso)
	class Meta:
		db_table = 'papeleria_detalle'

class Inventario(models.Model):	
	TIPO_MOVIMIENTO = (
		('I', 'Ingreso'), 
		('E', 'Egreso'),
	)

	fecha = models.DateTimeField(auto_now_add=True)
	tipoMovimiento = models.CharField(choices=TIPO_MOVIMIENTO, max_length=20)
	cantidad = models.IntegerField(blank=False)
	saldo = models.IntegerField(blank=False)
	empleado = models.ForeignKey('Empleado', db_column='empleado')
	sede = models.ForeignKey('Sede', db_column='sede')
	producto = models.ForeignKey('Producto', db_column='producto')
	def __str__(self):
		return u"Producto: %s Cantidad: %s" % (self.producto, self.saldo)
		return self.nombre
	class Meta:
		db_table = 'papeleria_inventario'