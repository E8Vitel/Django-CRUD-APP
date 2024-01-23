from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bodega.decorators import admin_required
from .forms import CustomAuthenticationForm, ProductoForm, SolicitudForm
from .models import DetalleSolicitud, Producto, Categoria, Historial, DetallesHistorial, Solicitud, Unidad, CategoriaUnidad
from datetime import datetime

# Create your views here.
def view_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('view_productos')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def view_logout(request):
    logout(request)
    return redirect('login')

@admin_required
def view_historial(request):
    historiales = Historial.objects.all()
    context = {'historiales': historiales}
    return render(request, 'historial.html', context)

@login_required
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

    context = {'categorias': categorias, 'productos': productos, 'categoria_filter': categoria_filter, 'producto_modal': None}

    return render(request, 'bodega.html', context)
@admin_required
def view_create_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    unidades = Unidad.objects.filter(categoria_unidad_id=1)
    return render(request, 'productos.html', {'productos': productos, 'categorias': categorias, 'unidades': unidades})

@admin_required
def view_create_existing_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    unidades = Unidad.objects.filter(categoria_unidad_id=1)
    return render(request, 'productosEx.html', {'productos': productos, 'categorias': categorias, 'unidades': unidades})

@login_required
def view_productos_output(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    unidades = Unidad.objects.filter(categoria_unidad_id=2)
    form = SolicitudForm()

    return render(request, 'salidaProd.html', {'productos': productos, 'categorias': categorias, 'unidades': unidades, 'form': form})

@login_required
def view_units(request):
    unidades = Unidad.objects.all()
    categorias = CategoriaUnidad.objects.all()
    return render(request, 'unidades.html', {'unidades': unidades, 'categorias': categorias})

@login_required
def view_solicitudes(request):
    if not request.user.is_staff:
        return redirect('/bodega/productos')

    solicitudes_pendientes = Solicitud.objects.filter(estado='pendiente')
    return render(request, 'solicitudes.html', {'solicitudes_pendientes': solicitudes_pendientes})

@admin_required
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
                nombre_producto=producto.nombre_producto,
                cantidad=producto.cantidad,
                precio_unitario=producto.precio,
                unidad=proveedor
            )

        return redirect('/bodega/productos')

    return render(request, 'bodega.html')

@admin_required
def create_existing_productos(request):
    productos = Producto.objects.all()

    if request.method == 'POST':
        productos_data = request.POST.getlist('productos[]')
        precios = request.POST.getlist('precios[]')
        cantidades = request.POST.getlist('cantidades[]')

        historial = Historial.objects.create(fecha=datetime.now())

        for producto_id, nuevo_precio, cantidad in zip(productos_data, precios, cantidades):
            producto_existente = Producto.objects.get(id=producto_id)

            detalle_historial = DetallesHistorial(
                historial=historial,
                producto=producto_existente,
                nombre_producto=producto_existente.nombre_producto,
                cantidad=int(cantidad),
                precio_unitario=float(nuevo_precio)
            )
            detalle_historial.save()

            producto_existente.precio = float(nuevo_precio)
            producto_existente.cantidad += int(cantidad)
            producto_existente.save()

        return redirect('/bodega/productos')

    return render(request, 'bodega.html', {'productos': productos})

@login_required   
def producto_output(request):
    if request.method == 'POST':
        usuario = request.user
        solicitud = Solicitud.objects.create(usuario=usuario, estado='pendiente')

        productos_seleccionados = request.POST.getlist('productos')
        cantidades = request.POST.getlist('cantidades')

        for producto_id, cantidad in zip(productos_seleccionados, cantidades):
            cantidad = int(cantidad)
            if cantidad > 0:
                producto = Producto.objects.get(pk=producto_id)
                DetalleSolicitud.objects.create(
                    solicitud=solicitud,
                    producto=producto,
                    cantidad=cantidad
                )

        messages.success(request, "Solicitud enviada correctamente.")
        return redirect('view_productos')

    productos = Producto.objects.all()
    return render(request, 'salidaProd.html', {'productos': productos})

@login_required
def create_unit(request):
    if request.method == 'POST':
        nombre_unidad = request.POST.get('nombre_unidad')
        categoria_unidad_id = request.POST.get('categoria_unidad')

        categoria_unidad = CategoriaUnidad.objects.get(id=categoria_unidad_id)

        Unidad.objects.create(
            nombre_Unidad=nombre_unidad,
            categoria_unidad=categoria_unidad
        )

        return redirect('../unidades')

    return render(request, 'unidades.html')

@admin_required
def edit_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect('view_productos')
        data['form'] = formulario
    
    return render(request, 'editProducto.html', data)

@admin_required
def delete_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.delete()
        return redirect('view_productos')

    return render(request, 'bodega.html', {'producto': producto})

@admin_required
def gestionar_solicitud(request, solicitud_id):
    if not request.user.is_staff:
        return redirect('view_productos')
    
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    if request.method == 'POST':
        if 'aceptar' in request.POST:
            solicitud.aceptada = True
            solicitud.estado = 'aceptada'
            solicitud.save()

            historial = Historial.objects.create(fecha=datetime.now(), receptor=solicitud.usuario)

            for detalle in solicitud.detalles_solicitud.all():
                DetallesHistorial.objects.create(
                    historial=historial,
                    producto=detalle.producto,
                    nombre_producto=detalle.producto.nombre_producto,
                    cantidad=detalle.cantidad,
                    precio_unitario=detalle.producto.precio
                )

                detalle.producto.cantidad -= detalle.cantidad
                detalle.producto.save()

            solicitud.delete()
            return redirect('view_solicitudes')
        elif 'denegar' in request.POST:
            solicitud.save()

            return redirect('view_solicitudes')
        
    return redirect('view_solicitudes')

@admin_required
def delete_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(DetalleSolicitud, id=solicitud_id)

    if request.method == 'POST':
        solicitud.delete()
        return redirect('view_solicitudes')

    return render(request, 'solicitudes.html', {'solicitudes': solicitudes})
