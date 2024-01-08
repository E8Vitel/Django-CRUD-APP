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

class DetalleHistorial(models.Model):
    fecha = models.DateTimeField()
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    Unidad = models.ForeignKey(Unidad, null=True, blank=True, on_delete=models.CASCADE)

