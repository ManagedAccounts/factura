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


@login_required
def facturaCrear(request):
    message = None
    mess_tipo = 0
    sqfactura = 1
    form = None
    return render_to_response('facturacion/crear_factura.html', {'message': message, 'form': form, 'mess_tipo': mess_tipo, 'sqfactura': sqfactura}, context_instance=RequestContext(request))
