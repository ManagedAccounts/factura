from django.contrib import admin
from .models import DetalleFactura, Factura, Producto, CategoriaProducto, Cliente
# Register your models here.


class DetalleFacturaInline(admin.TabularInline):
    model = DetalleFactura


class FacturaAdmin(admin.ModelAdmin):

    raw_id_fields = ('cliente',)
    inlines = (DetalleFacturaInline,)
    exclude = ['vendedor', ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.vendedor = request.user
        obj.save()


class ProductoAdmin(admin.TabularInline):
    model = Producto

admin.site.register(Factura, FacturaAdmin)

admin.site.register(Producto)
admin.site.register(CategoriaProducto)


class ClienteAdmin(admin.ModelAdmin):

    search_fields = ('razon_social', 'ruc',)
    list_display = (
        'razon_social', 'ruc', 'direccion', 'telefono',)

admin.site.register(Cliente, ClienteAdmin)
