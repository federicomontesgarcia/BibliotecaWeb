from django.shortcuts import render

from libros.models import Autor


# Create your views here.

def autores(request):

    autores = Autor.objects.all()

    return render(request, "autores/autores.html", {"autores": autores})


