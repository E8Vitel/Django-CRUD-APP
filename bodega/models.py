from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=255, unique=True)

class CategoriaUnidad(models.Model):
    categoria_unidad = models.CharField(max_length=255)

class Unidad(models.Model): 
    nombre_Unidad = models.CharField(max_length=255)
    categoria_unidad = models.ForeignKey(CategoriaUnidad, on_delete=models.CASCADE, null=False, blank=False)

class Producto(models.Model):
    nombre_producto = models.TextField(max_length=255)
    descripcion = models.TextField(max_length=255, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=False, blank=False)
    cantidad = models.IntegerField(null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    proveedor = models.ForeignKey(Unidad, on_delete=models.CASCADE, null=True, blank=True)
                              
class Historial(models.Model):
    fecha = models.DateTimeField()
    receptor = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True, blank=True)
    productos = models.ManyToManyField(Producto, through='DetallesHistorial')

class DetallesHistorial(models.Model):
    historial = models.ForeignKey(Historial, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
