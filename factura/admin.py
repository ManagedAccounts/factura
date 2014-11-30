from django.contrib import admin
from .models import DetalleFactura, Factura, Producto, CategoriaProducto, Cliente
# Register your models here.


class DetalleFacturaInline(admin.TabularInline):
    model = DetalleFactura

class FacturaAdmin(admin.ModelAdmin):
    inlines = (DetalleFacturaInline,)


class ProductoAdmin(admin.TabularInline):
    model = Producto

admin.site.register(Factura, FacturaAdmin)

admin.site.register(Producto)
admin.site.register(CategoriaProducto)
admin.site.register(Cliente)

