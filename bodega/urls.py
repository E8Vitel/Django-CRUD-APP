from django.urls import path
from .views import create_unit, create_producto, create_existing_productos, producto_output, view_login, view_logout, view_historial, view_productos, view_create_productos, view_create_existing_productos, view_productos_output, view_units
urlpatterns = [
    path('login', view_login, name='login'),
    path('logout/', view_logout, name='logout'),
    path('historial', view_historial),
    path('productos', view_productos, name='view_productos'),
    path('crear/nuevo', view_create_productos),
    path('crear/existente', view_create_existing_productos),
    path('crear/salida', view_productos_output),
    path('unidades', view_units),
    path('productos/', create_producto),
    path('existing_producto', create_existing_productos, name='existing_producto'),
    path('salida_producto', producto_output, name='salida_producto'),
    path('crear/unidades', create_unit, name='unidad')
]
