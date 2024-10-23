from django.shortcuts import render
from .models import Producto, Categoria
from .forms import ProductoForm

# Create your views here.

def index(request):
    context={}
    
    return render(request, 'pages/index.html', context)

def catalogo(request):
    producto = None
    if request.method == "POST":
        producto_id = request.POST.get('id_producto')
        if producto_id:
             producto = Producto.objects.get(id_producto=producto_id)
    

    return render(request, 'pages/catalogo.html', {'producto':producto})

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

        objCategoria = Categoria.objects.get(id_categoria = categoria)
        obj = Producto.objects.create(
            # id_producto =  id_prod,
            nom_producto = nombre,
            categoria = objCategoria,
            marca = marca,
            valor = valor,
        )
        obj.save()
        context = {
            "mensaje": "Registro exitoso",
        }
        return render(request, "pages/prod_add.html", context)
    
def producto_edit(request):
    if request.method == "POST":

        id_prod = request.POST.get("id_prod")
        nombre = request.POST.get("nombre")
        categoria = request.POST.get("categoria")
        marca = request.POST.get("marca")
        valor = request.POST.get("valor")

        # Validamos que todos los campos requeridos están presentes
        if not id_prod or not nombre or not categoria or not marca or not valor:
            # Manejo del error si falta alguno de los campos
            categorias = Categoria.objects.all()
            context = {
                "mensaje": "Error: Faltan datos en el formulario",
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

        # Obtener la categoría seleccionada
        objCategoria = Categoria.objects.get(id_categoria=categoria)

        # Actualizar los campos del producto existente
        producto.nom_producto = nombre  # Asegúrate de usar los nombres correctos de los campos
        producto.categoria = objCategoria
        producto.marca = marca
        producto.valor = valor

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

