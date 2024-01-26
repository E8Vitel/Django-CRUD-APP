from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from bodega.models import Producto, Solicitud, Unidad

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = None
        username = forms.CharField(label='Correo electrónico')
        password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
        fields = ['username', 'password']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'descripcion', 'categoria', 'cantidad', 'precio', 'proveedores']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()

        self.helper.layout = Layout(
            'nombre_producto',
            'descripcion',
            'categoria',
            'cantidad',
            'precio',
            'proveedor',
            Submit('submit', 'Guardar', css_class='btn-primary')
        )

        self.fields['nombre_producto'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Seleccione una categoría'})
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cantidad'})
        self.fields['precio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Precio'})

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'descripcion', 'categoria', 'cantidad', 'precio', 'proveedores']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()

        self.helper.layout = Layout(
            'nombre_producto',
            'descripcion',
            'categoria',
            'cantidad',
            'precio',
            'proveedores',
            Submit('submit', 'Guardar', css_class='btn-primary')
        )

        self.fields['nombre_producto'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'})
        self.fields['categoria'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Seleccione una categoría'})
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cantidad'})
        self.fields['precio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Precio'})

        self.fields['proveedores'].queryset = Unidad.objects.filter(categoria_unidad=1)

        self.fields['proveedores'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Proveedor'})


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['productos', 'cantidades']

    productos = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    cantidades = forms.CharField()