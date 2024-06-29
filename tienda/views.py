from django.shortcuts import render
from .models import Producto
from libros.models import Libro

# Create your views here.


def tienda(request):
    """Función para mostrar la información de los libros"""

    productos = Libro.objects.all()

    return render(request, "tienda/tienda.html", {"productos": productos})


