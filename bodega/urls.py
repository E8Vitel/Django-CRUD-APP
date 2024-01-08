from django.urls import path
from .views import create_producto, view_login, view_historial, view_productos

urlpatterns = [
    path('login', view_login),
    path('historial', view_historial),
    path('productos', view_productos),
    path('productos/', create_producto)
]
