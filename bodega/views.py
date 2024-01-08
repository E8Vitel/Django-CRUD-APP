from django.http import HttpResponse
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
        productos = []
        nombres = request.POST.getlist('nombreProducto[]')
        precios = request.POST.getlist('precio[]')
        cantidades = request.POST.getlist('cantidad[]')
        categorias = request.POST.getlist('categoria[]')

        # Asegúrate de que los campos tengan la misma longitud
        if len(nombres) == len(precios) == len(cantidades) == len(categorias):
            for i in range(len(nombres)):
                nombre = nombres[i]
                precio = float(precios[i])
                cantidad = int(cantidades[i])
                categoria_id = int(categorias[i])

                # Crea el objeto Producto y agrégalo a la lista
                productos.append(Producto(nombre_producto=nombre, precio=precio, stock=cantidad, categoria_id=categoria_id))

            # Guarda todos los productos en la base de datos
            Producto.objects.bulk_create(productos)


            # Crea objetos DetalleHistorial para cada producto y los vincula con el historial
            for producto in productos:
                detalle_historial = DetalleHistorial(
                    fecha=datetime.now(),
                    cantidad=producto.stock,
                    precio_unitario=producto.precio,
                    producto_id=producto,
                )
                detalle_historial.save()

    return redirect('/bodega/productos')


