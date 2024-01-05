from django.db import models

# Create your models here.
class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    contraseña = models.CharField(max_length=255)

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=255, unique=True)

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock = models.IntegerField()
    precio = models.FloatField()

class Historial(models.Model):
    historial_id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    receptor = models.CharField(max_length=255)

class DetalleHistorial(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    historial_id = models.ForeignKey(Historial, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)


