from django.shortcuts import render
from .models import Producto

# Create your views here.

def index(request):
    producto = None
    if request.method == "POST":
        producto_id = request.POST.get('id_producto')
        if producto_id:
             producto = Producto.objects.get(id_producto=producto_id)
    
    return render(request, 'main/index.html', {'producto':producto})