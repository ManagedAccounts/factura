# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    ruc=models.IntegerField(max_length=11, unique=True)
    razon_social=models.CharField(max_length=100)
    direccion=models.CharField(max_length=200)
    telefono=models.CharField(max_length=10)

    def __unicode__(self):
        return U"%s-%s" %(self.ruc,self.razon_social)

class CategoriaProducto(models.Model):
    nombre 	= models.CharField(max_length=200)
    descripcion = models.TextField(max_length=400)

    def __unicode__(self):
        return  u'%s' % (self.nombre)

class Producto(models.Model):
    # codigo = models.IntegerField()
    code = models.IntegerField()
    number = models.IntegerField()

    categoria = models.ForeignKey(CategoriaProducto)
    nombre = models.CharField(max_length=40)
    descripcion	= models.TextField(max_length=300)
    imagen = models.ImageField(upload_to="productos/",null=True,blank=True)
    precio = models.DecimalField(max_digits=6,decimal_places=2)
    afecto = models.BooleanField(default=False)
    igv = models.DecimalField(max_digits=6,decimal_places=2)
    stock = models.IntegerField()
    estado = models.BooleanField(default=True)

    # def get_serial_number(self):
    #     "Get formatted value of serial number"
    #     return "%.2d-%.3d" % (self.code, self.number)

    # def save(self):
    #     "Get last value of Code and Number from database, and increment before save"
    #     top = Producto.objects.order_by('-code','-producto')[0]
    #     self.code = top.code + 1
    #     self.number = top.number + 1
    #     super(Producto, self).save()

    def __unicode__(self):
        return  u'%s-%s' % (self.code,self.nombre)

class Factura(models.Model):
    serie=models.IntegerField(max_length=3)
    numero=models.CharField(max_length=6, unique=True)
    cliente=models.ForeignKey(Cliente)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(null=True, blank=True)
    vendedor=models.ForeignKey(User)

    def __unicode__(self):
        return U" %s- %s" %(self.cliente, self.fecha)

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, db_column='factura_id')
    producto = models.ForeignKey(Producto, db_column='producto_id')
    cantidad = models.IntegerField()
    impuesto = models.DecimalField(max_digits=6,decimal_places=2)
    subtotal = models.DecimalField(max_digits=6,decimal_places=2)

    def __unicode__(self):
        return u'%s' %  self.subtotal



