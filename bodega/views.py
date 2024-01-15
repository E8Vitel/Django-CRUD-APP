from gettext import translation
from django.shortcuts import redirect, render
from .models import Producto, Categoria, Historial, DetallesHistorial, Unidad
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
        producto.precio_total = producto.stock * producto.precio
        
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
    return render(request, 'unidades.html', {'unidades': unidades})

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

def update_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('id')
        cantidad_nueva = int(request.POST.get('cantidad_nueva'))
        nuevo_precio = float(request.POST.get('nuevo_precio'))

        producto_existente = Producto.objects.get(id=producto_id)

        producto_existente.stock += cantidad_nueva
        producto_existente.precio = nuevo_precio
        producto_existente.save()

        historial = Historial.objects.get(fecha=datetime.now())

        DetallesHistorial.objects.create(
            historial=historial,
            producto=producto_existente,
            cantidad=cantidad_nueva,
            precio_unitario=nuevo_precio
        )

        return redirect('/bodega/productos')

def producto_output(request):
    return redirect('/bodega/productos')