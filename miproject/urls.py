from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

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
    url(r'^factura/buscar_cliente$', 'apps.factura.views.buscarCliente'),
    url(r'^factura/buscar_producto$', 'apps.factura.views.buscarProducto'),

    url(r'^factura/consultar$', 'apps.factura.views.consultarFactura', name="consultar_factura"),

    #==================================================================
    url(r'^clientes/$','apps.factura.views.clientes'),
    url(r'^clienteAdd/$','apps.factura.views.clienteAdd'),
    url(r'^clienteEdit/(?P<id>\d+)$','apps.factura.views.clienteEdit'),
    url(r'^clienteDelete/(?P<id>\d+)$','apps.factura.views.clienteDelete'),
    url(r'^productos/$','apps.factura.views.productos'),
    url(r'^productoAdd/$','apps.factura.views.productoAdd'),
    url(r'^productoEdit/(?P<id>\d+)$','apps.factura.views.productoEdit'),
    url(r'^productoDelete/(?P<id>\d+)$','apps.factura.views.productoDelete'),
    url(r'^categoria/$','apps.factura.views.categoria'),
    url(r'^categoriaAdd/$','apps.factura.views.categoriaAdd'),
    url(r'^categoriaEdit/(?P<id>\d+)$','apps.factura.views.categoriaEdit'),
    url(r'^categoriaDelete/(?P<id>\d+)$','apps.factura.views.categoriaDelete'),

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
