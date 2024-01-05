from django.shortcuts import render

# Create your views here.
def view_login(request):
    return render(request, 'index.html')

def view_historial(request):
    return render(request, 'historial.html')

def view_productos(request):
    return render(request, 'bodega.html')

