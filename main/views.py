from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login as auth_login
from .models import Producto, Categoria
from transbank.webpay.webpay_plus.transaction import Transaction
from django.conf import settings

# Create your views here.

def grupo_cliente(user):
    return user.groups.filter(name='cliente').exists()

def grupo_inventario(user):
    return user.groups.filter(name='inventario').exists()

def index(request):
    context={}
    
    return render(request, 'pages/index.html', context)

def carrito(request):
    context={}

    return render(request,'pages/carrito.html',context)

def catalogo(request):
    producto = None
    if request.method == "POST":
        producto_id = request.POST.get('id_producto')
        if producto_id:
             producto = Producto.objects.get(id_producto=producto_id)
    

    return render(request, 'pages/catalogo.html', {'producto':producto})

def herramientas(request):
    context={

    }
    return render(request,'pages/herramientas.html',context)

def muebles(request):
    context={

    }
    return render(request,'pages/muebles.html',context)

def seguridad(request):
    context={

    }
    return render(request,'pages/seguridad.html',context)

def proteccion(request):
    context={

    }
    return render(request,'pages/proteccion.html',context)


def inventario(request):
    productos = Producto.objects.all()
    context= {
        "productos":productos,
    }
    return render(request, "pages/inventario.html", context)

def prod_findEdit (request,pk):
    if pk != "":
        producto = Producto.objects.get(id_producto=pk)
        categorias = Categoria.objects.all()
        context = {
            "categorias":categorias,
            "producto":producto,
        }
        return render(request, "pages/producto_edit.html", context)
    else:
        producto = Producto.objects.all()
        context = {
            "mensaje":"Error, producto no encontrado",
            "producto":producto
        }
        return render(request, "pages/inventario.html", context)
    
def prod_del(request, pk):
    try:
        producto = Producto.objects.get(id_producto=pk)
        producto.delete()
        productos = Producto.objects.all()
        context = {
            "mensaje":"Eliminado con exito",
            "productos": productos,
        }
        return render(request, "pages/inventario.html", context)
    except:
        productos = Producto.objects.all()
        context = {
            "mensaje": "Error, producto no encontrado...",
            "productos": productos,
        }
        return render(request, "pages/inventario.html", context)
    
def prod_add(request):
    if request.method != "POST":
        categorias = Categoria.objects.all()
        context = {
            "categorias":categorias,
        }
        return render(request,"pages/prod_add.html", context)
    else:
        # id_prod = request.POST["id_prod"]
        nombre = request.POST["nombre"]
        categoria = request.POST["categoria"]
        marca = request.POST["marca"]
        valor = request.POST["valor"]
        stock = request.Post["stock"]

        objCategoria = Categoria.objects.get(id_categoria = categoria)
        obj = Producto.objects.create(
            # id_producto =  id_prod,
            nom_producto = nombre,
            categoria = objCategoria,
            marca = marca,
            valor = valor,
            stock = stock,
        )
        obj.save()
        context = {
            "mensaje": "Registro exitoso",
        }
        return render(request, "pages/prod_add.html", context)
    
def producto_edit(request):
    if request.method == "POST":

        id_prod = request.POST.get("id_prod")
        
        # Verificamos si el ID del producto está presente
        if not id_prod:
            categorias = Categoria.objects.all()
            context = {
                "mensaje": "Error: Producto no especificado",
                "categorias": categorias,
            }
            return render(request, "pages/producto_edit.html", context)

        # Obtener el producto existente por su ID
        try:
            producto = Producto.objects.get(id_producto=id_prod)  # Busca el producto a modificar
        except Producto.DoesNotExist:
            # Si no existe el producto, mostramos un error
            categorias = Categoria.objects.all()
            context = {
                "mensaje": "Error: Producto no encontrado",
                "categorias": categorias,
            }
            return render(request, "pages/producto_edit.html", context)

        if 'modificar_nombre' in request.POST:
            nombre = request.POST.get("nombre")
            if nombre:
                producto.nom_producto = nombre

        elif 'modificar_categoria' in request.POST:
            categoria_id = request.POST.get("categoria")
            if categoria_id:
                objCategoria = Categoria.objects.get(id_categoria=categoria_id)
                producto.categoria = objCategoria

        elif 'modificar_marca' in request.POST:
            marca = request.POST.get("marca")
            if marca:
                producto.marca = marca

        elif 'modificar_valor' in request.POST:
            valor = request.POST.get("valor")
            if valor:
                producto.valor = valor

        elif 'modificar_stock' in request.POST:
            stock = request.POST.get("stock")
            if stock:
                producto.stock = stock

        # Guardar el producto modificado
        producto.save()

        # Obtener todas las categorías para pasarlas al contexto
        categorias = Categoria.objects.all()
        context = {
            "mensaje": "Modificado con éxito",
            "categorias": categorias,
            "producto": producto,
        }
        return render(request, "pages/producto_edit.html", context)

    else:
        # En caso de que no sea un POST
        categorias = Categoria.objects.all()
        context = {
            "categorias": categorias,
        }
        return render(request, "pages/producto_edit.html", context)

def login(request):

    return render(request, 'pages/login.html')

def logout(request):
    logout(request)
    return redirect('pages/login.html')

def exito(request):

    return render(request, 'pages/success.html')

def mal(request):

    return render(request, 'pages/failure.html')

def pagar(request):
    transaction = Transaction()
    transaction.commerce_code = settings.TRANSBANK_COMMERCE_CODE
    transaction.api_key = settings.TRANSBANK_API_KEY
    transaction.enviroment = settings.TRANSBANK_ENVIRONMENT

    response = transaction.create(
        buy_order='order12345',
        session_id='session12345',
        amount=10000,
        return_url='http://127.0.0.1:8000/main/transaccion_completa'
    )
    print(response)
    return redirect(response['url'] + '?token_ws=' + response['token'])

def transaccion_completa(request):
    token_ws = request.GET.get('token_ws')
    transaction = Transaction()
    try:
        result = transaction.commit(token_ws)
        if result['status'] == 'AUTHORIZED':
            return render(request, 'pages/success.html')
        else:
            reason = result.get('status', 'Unknown reason')
            return render(request, 'pages/failure.html', {'reason': reason, 'result': result})
    except Exception as e:
        return render(request, 'pages/failure.html', {'reason': str(e)})