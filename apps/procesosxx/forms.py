from django import forms
from apps.procesos.models import Proceso, Producto

class ProcesoForm(forms.ModelForm):
	class Meta:
		model = Proceso

class ProductoForm(forms.ModelForm):
	class Meta:
		model = Producto