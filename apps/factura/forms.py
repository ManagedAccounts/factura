from django import forms
from .models import Cliente, Producto, CategoriaProducto
from django.forms import ModelForm


class ClienteForm(ModelForm):
    class Meta:
        model=Cliente
        fields=['ruc','razon_social','direccion','telefono']

class ProductoForm(ModelForm):
    class Meta:
        model=Producto
        exclude=['igv']
        fields=['code','number','categoria','nombre','descripcion','imagen','precio','afecto','igv','stock','estado']

class CategoriaForm(ModelForm):
    class Meta:
        model=CategoriaProducto
        fields=['nombre','descripcion']

