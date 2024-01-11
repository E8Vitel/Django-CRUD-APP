from gettext import translation
from django.shortcuts import redirect, render
from .models import Producto, Categoria, Historial, DetallesHistorial
from datetime import datetime
# Create your views here.
def view_login(request):
    return render(request, 'index.html')

def view_historial(request):
    historiales = Historial.objects.all()
    context = {'historiales': historiales}
    return render(request, 'historial.html', context)

def view_productos(request):
    categorias = Categoria.objects.all()
    categoria_filter = request.GET.get('categoria', 'todo')

    if categoria_filter != 'todo':
        productos = Producto.objects.filter(categoria_id=categoria_filter)
    else:
        productos = Producto.objects.all()

    return render(request, 'bodega.html', {'categorias': categorias, 'productos': productos, 'categoria_filter': categoria_filter})


def create_producto(request):
    if request.method == 'POST':
        nombres = request.POST.getlist('nombreProducto[]')
        descripciones = request.POST.getlist('description[]')
        precios = request.POST.getlist('precio[]')
        cantidades = request.POST.getlist('cantidad[]')
        categorias_ids = request.POST.getlist('categoria[]')

        # Create a new Historial object only once
        historial = Historial.objects.create(fecha=datetime.now())

        for nombre, descripcion, precio, cantidad, categoria_id in zip(nombres, descripciones, precios, cantidades, categorias_ids):
            categoria = Categoria.objects.get(id=categoria_id)
            producto = Producto.objects.create(
                nombre_producto=nombre,
                descripcion=descripcion,
                precio=float(precio),
                stock=int(cantidad),
                categoria=categoria
            )

            # Associate the product with the previously created Historial
            DetallesHistorial.objects.create(
                historial=historial,
                producto=producto,
                cantidad=producto.stock,
                precio_unitario=producto.precio
            )

        # Redirect to the page after all products are processed
        return redirect('/bodega/productos')

    return render(request, 'bodega.html')