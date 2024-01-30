from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gasto_acumulado = models.FloatField(default=0.0)

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.nombre_categoria

class Unidad(models.Model): 
    nombre_Unidad = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre_Unidad
    
class Producto(models.Model):
    nombre_producto = models.TextField(max_length=255)
    descripcion = models.TextField(max_length=255, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=False, blank=False)
    cantidad = models.IntegerField(null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    proveedores = models.ManyToManyField(Unidad, through='producto_proveedor')
    def __str__(self):
        return self.nombre_producto
                              
class producto_proveedor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Unidad, on_delete=models.CASCADE)
class Historial(models.Model):
    fecha = models.DateTimeField()
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    productos = models.ManyToManyField(Producto, through='DetallesHistorial')

class DetallesHistorial(models.Model):
    historial = models.ForeignKey(Historial, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    nombre_producto = models.CharField(max_length=255, null=True, blank=True)  
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
    unidad = models.CharField(max_length=255, null=True, blank=True)

class Solicitud(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='DetalleSolicitud')
    estado = models.CharField(max_length=20, default='pendiente')

class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='detalles_solicitud')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()