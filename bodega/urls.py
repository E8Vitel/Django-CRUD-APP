from django.urls import path
from .views import edit_unidad, delete_unidad, create_unit, create_producto, create_existing_productos, delete_producto, delete_solicitud, descargar_historial, edit_producto, gestionar_solicitud, modificar_cantidad, producto_output, view_login, view_logout, view_historial, view_productos, view_create_productos, view_create_existing_productos, view_productos_output, view_solicitudes, view_units, obtener_producto_excel
urlpatterns = [
    path('', view_login, name='login'),
    path('logout/', view_logout, name='logout'),
    path('historial', view_historial, name='view_historial'),
    path('productos', view_productos, name='view_productos'),
    path('crear/nuevo', view_create_productos, name='view_create_productos'),
    path('crear/existente', view_create_existing_productos, name='view_existing_productos'),
    path('crear/salida', view_productos_output, name='view_productos_output'),
    path('unidades', view_units, name='view_unidades'),
    path('solicitudes', view_solicitudes, name='view_solicitudes'),
    path('productos/', create_producto, name='create_producto'),
    path('existing_producto', create_existing_productos, name='existing_producto'),
    path('salida_producto', producto_output, name='salida_producto'),
    path('crear/unidades', create_unit, name='unidad'), 
    path('descargar_historial/', descargar_historial, name='descargar_historial'),
    path('descargar_productos/', obtener_producto_excel, name='descargar_productos'),
    path('productos/editar/<int:producto_id>', edit_producto, name='edit_producto'),
    path('productos/eliminar/<int:producto_id>', delete_producto, name='delete_producto'),
    path('gestionar_solicitud/<int:solicitud_id>/', gestionar_solicitud, name='gestionar_solicitud'),
    path('modificar_cantidad/<int:solicitud_id>/<int:producto_id>/', modificar_cantidad, name='modificar_cantidad'),
    path('eliminar_solicitud/<int:solicitud_id>/', delete_solicitud, name='eliminar_solicitud'),
    path('unidades/editar/<int:unidad_id>', edit_unidad, name='edit_unidad'),
    path('unidades/eliminar/<int:unidad_id>', delete_unidad, name='delete_unidad'),
]

