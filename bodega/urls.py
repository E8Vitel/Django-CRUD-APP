from django.urls import path
from .views import create_producto, update_producto, producto_output, view_login, view_historial, view_productos, view_create_productos, view_create_existing_productos, view_productos_output, view_units
urlpatterns = [
    path('login', view_login),
    path('historial', view_historial),
    path('productos', view_productos),
    path('crear/nuevo', view_create_productos),
    path('crear/existente', view_create_existing_productos),
    path('crear/salida', view_productos_output),
    path('unidades', view_units),
    path('productos/', create_producto),
    path('productos/', update_producto),
    path('productos/', producto_output)
]
