from django.db import models

# Create your models here.
class Usuario(models.Model):
    email = models.TextField(max_length=255, unique=True)
    contraseña = models.CharField(max_length=40)

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=255, unique=True)

class Producto(models.Model):
    nombre_producto = models.TextField(max_length=255)
    descripcion = models.TextField(max_length=255, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=False, blank=False)
    stock = models.IntegerField()
    precio = models.FloatField()

class Unidad(models.Model): 
    nombre_Unidad = models.CharField(max_length=255)

class Historial(models.Model):
    fecha = models.DateTimeField()
    receptor = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True, blank=True)
    productos = models.ManyToManyField(Producto, through='DetallesHistorial')

class DetallesHistorial(models.Model):
    historial = models.ForeignKey(Historial, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
