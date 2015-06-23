from django import forms
from .models import Cliente, Producto, CategoriaProducto
from django.forms import ModelForm


class ClienteForm(ModelForm):
    class Meta:
        model=Cliente

class ProductoForm(ModelForm):
    class Meta:
        model=Producto
        exclude=['igv']

class CategoriaForm(ModelForm):
    class Meta:
        model=CategoriaProducto

