from gettext import translation
from django.shortcuts import redirect, render
from .models import Producto, Categoria, Historial, DetallesHistorial, Unidad, CategoriaUnidad
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
    productos = Producto.objects.all()
    
    if categoria_filter != 'todo':
        productos = Producto.objects.filter(categoria_id=categoria_filter)
    else:
        productos = Producto.objects.all()

    for producto in productos:
        producto.precio_total = producto.cantidad * producto.precio
        
    return render(request, 'bodega.html', {'categorias': categorias, 'productos': productos, 'categoria_filter': categoria_filter})

def view_create_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'productos.html', {'productos': productos, 'categorias': categorias})

def view_create_existing_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'productosEx.html', {'productos': productos, 'categorias': categorias})

def view_productos_output(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'salidaProd.html', {'productos': productos, 'categorias': categorias})

def view_units(request):
    unidades = Unidad.objects.all()
    categorias = CategoriaUnidad.objects.all()
    return render(request, 'unidades.html', {'unidades': unidades, 'categorias': categorias})

def create_producto(request):
    if request.method == 'POST':
        nombres = request.POST.getlist('nombreProducto[]')
        descripciones = request.POST.getlist('description[]')
        precios = request.POST.getlist('precio[]')
        cantidades = request.POST.getlist('cantidad[]')
        categorias_ids = request.POST.getlist('categoria[]')

        historial = Historial.objects.create(fecha=datetime.now())

        for nombre, descripcion, precio, cantidad, categoria_id in zip(nombres, descripciones, precios, cantidades, categorias_ids):
            categoria = Categoria.objects.get(id=categoria_id)
            producto = Producto.objects.create(
                nombre_producto=nombre,
                descripcion=descripcion,
                precio=float(precio),
                cantidad=int(cantidad),
                categoria=categoria
            )

            DetallesHistorial.objects.create(
                historial=historial,
                producto=producto,
                cantidad=producto.cantidad,
                precio_unitario=producto.precio
            )

        # Redirect to the page after all products are processed
        return redirect('/bodega/productos')

    return render(request, 'bodega.html')

def update_producto(request):
    productos = Producto.objects.all()

    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        nuevo_precio = float(request.POST.get('precio'))
        cantidad = int(request.POST.get('cantidad'))

        producto_existente = Producto.objects.get(id=producto_id)

        DetallesHistorial.objects.create(
            historial=Historial.objects.create(fecha=datetime.now()),
            producto=producto_existente,
            cantidad=cantidad,
            precio_unitario=nuevo_precio
        )

        producto_existente.precio = nuevo_precio
        producto_existente.cantidad += cantidad
        producto_existente.save()

        return redirect('/bodega/productos')
    return render(request, 'bodega.html', {'productos': productos})
    
def producto_output(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))
        receptor = request.POST.get('receptor')

        producto_output = Producto.objects.get(id=producto_id)

        DetallesHistorial.objects.create(
            historial=Historial.objects.create(fecha=datetime.now()),
            producto=producto_output,
            cantidad=cantidad,
            precio_unitario=producto_output.precio,
            receptor=receptor
        )

        producto_output.cantidad -= cantidad
        producto_output.save()

        return redirect('/bodega/productos')