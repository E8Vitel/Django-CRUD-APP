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
    query = request.GET.get('q', '')

    if categoria_filter != 'todo':
        productos = Producto.objects.filter(categoria_id=categoria_filter, nombre_producto__icontains=query)
    else:
        productos = Producto.objects.filter(nombre_producto__icontains=query)

    for producto in productos:
        producto.precio_total = producto.cantidad * producto.precio
        
    return render(request, 'bodega.html', {'categorias': categorias, 'productos': productos, 'categoria_filter': categoria_filter})

def view_create_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    unidades = Unidad.objects.filter(categoria_unidad_id=1)
    return render(request, 'productos.html', {'productos': productos, 'categorias': categorias, 'unidades': unidades})

def view_create_existing_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    unidades = Unidad.objects.filter(categoria_unidad_id=1)
    return render(request, 'productosEx.html', {'productos': productos, 'categorias': categorias, 'unidades': unidades})

def view_productos_output(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    unidades = Unidad.objects.filter(categoria_unidad_id=2)
    return render(request, 'salidaProd.html', {'productos': productos, 'categorias': categorias, 'unidades': unidades})

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
        proveedores_ids = request.POST.getlist('proveedor[]')

        historial = Historial.objects.create(fecha=datetime.now())

        for nombre, descripcion, precio, cantidad, categoria_id, proveedor_id in zip(nombres, descripciones, precios, cantidades, categorias_ids, proveedores_ids):
            categoria = Categoria.objects.get(id=categoria_id)
            proveedor = Unidad.objects.get(id=proveedor_id)
            producto = Producto.objects.create(
                nombre_producto=nombre,
                descripcion=descripcion,
                precio=float(precio),
                cantidad=int(cantidad),
                categoria=categoria,
                proveedor=proveedor
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
        productos_data = request.POST.getlist('producto')
        precios = request.POST.getlist('precio')
        cantidades = request.POST.getlist('cantidad')

        historial = Historial.objects.create(fecha=datetime.now())

        for producto_id, nuevo_precio, cantidad in zip(productos_data, precios, cantidades):
            producto_existente = Producto.objects.get(id=producto_id)

            DetallesHistorial.objects.create(
                historial=historial,
                producto=producto_existente,
                cantidad=int(cantidad),
                precio_unitario=float(nuevo_precio),
            )

        producto_existente.precio = nuevo_precio
        producto_existente.cantidad += cantidad
        producto_existente.save()

        return redirect('/bodega/productos')
    return render(request, 'bodega.html', {'productos': productos})
    
def producto_output(request):
    productos = Producto.objects.all()
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
    return render(request, 'bodega.html', {'productos': productos})

def create_unit(request):
    if request.method == 'POST':
        nombre_unidad = request.POST.get('nombre_unidad')
        categoria_unidad_id = request.POST.get('categoria_unidad')

        # Obtener la categoría de la unidad
        categoria_unidad = CategoriaUnidad.objects.get(id=categoria_unidad_id)

        # Crear la unidad con la categoría
        Unidad.objects.create(
            nombre_Unidad=nombre_unidad,
            categoria_unidad=categoria_unidad
        )

        # Redirigir a la página de unidades o a donde desees
        return redirect('../unidades')

    return render(request, 'unidades.html')