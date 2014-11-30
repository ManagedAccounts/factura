from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'miproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'apps.login.views.homepage', name="homepage"),
    url(r'^login/$', 'apps.login.views.login_page', name="login"),
    url(r'^logout/$', 'apps.login.views.logout_view', name="logout"),


    url(r'^factura/venta$', 'apps.factura.views.facturaCrear',
        name="factura_venta"),




)


"""
    url(r'^facturacion/orden$', 'apps.procesos.views.ordenCompraCrea', name="orden_compra"),
    url(r'^facturacion/remision$', 'apps.procesos.views.remisionCompraCrea', name="remision_compra"),

    url(r'^facturacion/buscar_cliente$', 'apps.procesos.views.buscarCliente'),
    url(r'^facturacion/buscar_proveedor$', 'apps.procesos.views.buscarProveedor'),

    url(r'^facturacion/buscar_producto$', 'apps.procesos.views.buscarProducto'),
    url(r'^facturacion/secuencia_item$', 'apps.procesos.views.ejecutarSecuencia'),
    url(r'^facturacion/descuento$', 'apps.procesos.views.descuentoProducto'),

    url(r'^facturacion/buscar_orden$', 'apps.procesos.views.buscarOrdenCompra'),
    url(r'^facturacion/buscar_orden_detalle$', 'apps.procesos.views.buscarOrdenDetalle'),

    url(r'^inventario/consultar$', 'apps.procesos.views.consultarIntentario', name="consultar_inventario"),    

    url(r'^producto/crear$', 'apps.procesos.views.productoCrear', name="crear_producto"),
"""