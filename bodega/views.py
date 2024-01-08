from django.shortcuts import redirect, render
from .models import Producto, Categoria, DetalleHistorial
from datetime import datetime
# Create your views here.
def view_login(request):
    return render(request, 'index.html')

def view_historial(request):
    return render(request, 'historial.html')

def view_productos(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    return render(request, 'bodega.html', {'categorias': categorias, 'productos': productos})

def create_producto(request):
    if request.method == 'POST':
        nombres = request.POST.getlist('nombreProducto[]')
        descripciones = request.POST.getlist('description[]')
        precios = request.POST.getlist('precio[]')
        cantidades = request.POST.getlist('cantidad[]')
        categorias_ids = request.POST.getlist('categoria[]')

        productos_creados = 0
        for nombre, descripcion, precio, cantidad, categoria_id in zip(nombres, descripciones, precios, cantidades, categorias_ids):

                categoria = Categoria.objects.get(id=categoria_id)
                producto = Producto.objects.create(
                    nombre_producto=nombre,
                    descripcion=descripcion,
                    precio=float(precio),
                    stock=int(cantidad),
                    categoria=categoria
                )
                DetalleHistorial.objects.create(
                    fecha=datetime.now(),
                    cantidad=producto.stock,
                    precio_unitario=producto.precio,
                    producto_id=producto
                )
                productos_creados += 1

        return redirect('/bodega/productos')
    return render(request, 'bodega.html')