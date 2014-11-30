from django.contrib import admin
from apps.procesos.models import Categoria, Sede, TipoIdentificacion, Cargo, Empleado, Tipo, ClienteProveedor, Producto, Descuento, Telefono, TipoProceso, Proceso, Detalle, Inventario

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Sede)
admin.site.register(TipoIdentificacion)
admin.site.register(Cargo)
admin.site.register(Empleado)
admin.site.register(Tipo)
admin.site.register(ClienteProveedor)
admin.site.register(Producto)
admin.site.register(Descuento)
admin.site.register(Telefono)
admin.site.register(TipoProceso)
admin.site.register(Proceso)
admin.site.register(Detalle)
admin.site.register(Inventario)

