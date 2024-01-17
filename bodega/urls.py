from django.urls import path
from .views import create_unit, create_producto, update_producto, producto_output, view_login, view_historial, view_productos, view_create_productos, view_create_existing_productos, view_productos_output, view_units
urlpatterns = [
    path('', view_login),
    path('historial', view_historial),
    path('productos', view_productos, name='view_productos'),
    path('crear/nuevo', view_create_productos),
    path('crear/existente', view_create_existing_productos),
    path('crear/salida', view_productos_output),
    path('unidades', view_units),
    path('productos/', create_producto),
    path('modificar_producto', update_producto, name='modificar_producto'),
    path('salida_producto', producto_output, name='salida_producto'),
    path('crear/unidades', create_unit, name='unidad')
]
