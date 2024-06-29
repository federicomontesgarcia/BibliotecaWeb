from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LibroSerializer, AutorSerializer, GeneroSerializer
from .models import Libro, Autor, Genero
import requests
from django.http import JsonResponse
from django.contrib import messages


import json
# Create your views here.

def libros(request):
    """Se obtiene listado de los libros y se muestra en la vista""" 

    libros = Libro.objects.all()
    autores = Autor.objects.all()
    generos = Genero.objects.all()

    return render(request, "libros/libros.html",
                  {"libros": libros, "autores": autores, "generos": generos})


@api_view(["POST"])
@permission_classes((AllowAny,))
def save_book(request):
   
    
    if request.method == 'POST':
        try:
            data = request.data  # Accede directamente a los datos enviados en la solicitud POST

            bookName = data.get('bookName', '')
            author = int(data.get('author', ''))
            gender = int(data.get('gender', ''))
            editorial = data.get('editorial', '')
            year = data.get('year', '')
            price = data.get('price', '')
            image = request.FILES.get('image', None)

            try:
                author = Autor.objects.get(id=author)
                gender = Genero.objects.get(id=gender)
            
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Autor o Género no encontrado'}, status=400)

            libro = Libro(
                nombre = bookName,
                autor = author,
                genero = gender,
                editorial = editorial,
                fecha = year,
                precio = price,
                imagen = image
            )
            libro.save()
            messages.success(request, 'El libro se agregó satisfactoriamente.')
            return redirect('Libros')
        except Exception as e:
            return JsonResponse({'error': 'Error al procesar los datos'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def eliminar_libro(request, id_libro):

    libro = Libro.objects.get(id = id_libro)
    libro.delete()
    messages.success(request, 'El libro se eliminó satisfactoriamente.')

    libros = Libro.objects.all()
    autores = Autor.objects.all()
    generos = Genero.objects.all()

    return render(request, "libros/libros.html",
                  {"libros": libros, "autores": autores, "generos": generos})


def editar_libro(request, id_libro):

    querysetLibro = Libro.objects.filter(id = id_libro).values('id', 'nombre', 'precio', 'editorial', 'fecha', 'autor', 'genero', 'imagen')
    libro = list(querysetLibro)
   
    querysetAutor = Autor.objects.filter(id = libro[0]['autor']).values('nombre', 'apellido')
    autor = list(querysetAutor)
    libro[0]['autor'] = " ".join([autor[0]['nombre'], autor[0]['apellido']]) 
    
    querysetGenero = Genero.objects.filter(id = libro[0]['genero']).values('nombre')
    genero = list(querysetGenero)
    libro[0]['genero'] = genero[0]['nombre']
    
    autores = Autor.objects.all()
    generos = Genero.objects.all()

    context = {"data": libro, "autores": autores, "generos": generos}
    return render(request, 'libros/editar_libro.html', context)


@api_view(["POST"])
@permission_classes((AllowAny,))
def save_book_edit(request):
    """function to save books."""

    if request.method == 'POST':
        try:
            data = request.data  # Accede directamente a los datos enviados en la solicitud POST
            
            id = data.get('id', '')
            image = data.get('imagen', '')

            bookName = data.get('bookName', '')
           
            author = (data.get('author', ''))
            author = author.split()
            nombre = author[0]
            apellido = author[1]
            author_id = Autor.objects.filter(nombre = nombre, apellido = apellido).values('id')
            
            author = (author_id[0]['id'])
            gender = (data.get('gender', ''))
            gender_id = Genero.objects.filter(nombre = gender).values('id')
            gender = gender_id[0]['id']
            
            editorial = data.get('editorial', '')
          
            year = data.get('year', '')
           
            price = data.get('price', '')
            price = price.replace(',', '.')
            price = float(price)
            
            try:
                author = Autor.objects.get(id=author)
                gender = Genero.objects.get(id=gender)
            
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Autor o Género no encontrado'}, status=400)

            libro = Libro(
                id = id,
                nombre = bookName,
                autor = author,
                genero = gender,
                editorial = editorial,
                fecha = year,
                precio = price,
                imagen = image
            )
            libro.save()
            messages.success(request, 'El libro se actualizó satisfactoriamente.')
            return redirect('Libros')
        except Exception as e:
            return JsonResponse({'error': 'Error al procesar los datos'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
   
    
# --- API --------

class LibroViews(APIView):
    #
    serializer_class = LibroSerializer

    def get_queryset(self):
        print("libro fede")
        return Libro.objects.select_related('autor').all()

    def post(self, request):
        print("entra en post")
        print(request.data)
        serializer = LibroSerializer(data=request.data)

        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, id=None):
        if id:
            item = Libro.objects.select_related('autor').get(id=id)

            serializer = LibroSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Libro.objects.select_related('autor', 'genero').all()
       
        datos_modificados = []

        # Iterar sobre cada libro y agregarlo a la lista con el código del autor en lugar del nombre
        for item in items:
            # Crear un nuevo diccionario con los datos del libro
            libro_modificado = {
                "id": item.id,
                "nombre": item.nombre,
                "precio": item.precio,
                "editorial": item.editorial,
                "fecha": item.fecha,
                "autor": " ".join([item.autor.nombre, item.autor.apellido]),  # Reemplazar el nombre del autor por el código del autor
                "genero": item.genero.nombre,
                #"imagen": item.imagen
            }
            datos_modificados.append(libro_modificado)

        # Crear un diccionario con el estado y los datos modificados
        resultado = {
            "status": "success",
            "data": datos_modificados
        }

        #print(resultado)
        return Response({"status": "success", "data": resultado}, status=status.HTTP_200_OK)

        """
        # Convertir el resultado a JSON
        resultado_json = json.dumps(resultado, indent=4)

        print(resultado_json)

        serializer = LibroSerializer(resultado_json, many=True)
        print(serializer)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        """
    def patch(self, request, id=None):
        item = Libro.objects.get(id=id)
        serializer = LibroSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(Libro, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


class AutorViews(APIView):
    serializer_class = AutorSerializer

    def get_queryset(self):
        return Autor.objects.all()

    def post(self, request):
        serializer = AutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, id=None):
        if id:
            item = Autor.objects.get(id=id)
            serializer = AutorSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Autor.objects.all()
        serializer = AutorSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        item = Autor.objects.get(id=id)
        serializer = AutorSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(Autor, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


class GeneroViews(APIView):
    serializer_class = GeneroSerializer

    def get_queryset(self):
        return Genero.objects.all()

    def post(self, request):
        serializer = GeneroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, id=None):
        if id:
            item = Genero.objects.get(id=id)
            print("item")
            print(item)
            serializer = GeneroSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Genero.objects.all()
        serializer = GeneroSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        item = Genero.objects.get(id=id)
        serializer = GeneroSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(Genero, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


    #--- GOOGLE API BOOKS ---

class LibrosViews(APIView):

    def get(self, request, clave_api='AIzaSyCIUpw80bNcmyZZmVemB49yQcrViWjVvjs'):
        print("entra en Libros Views")
        autor = "victor del arbol"
        #url = f"https://www.googleapis.com/books/v1/volumes?q={titulo}&key={clave_api}"

        url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{autor}&key={clave_api}"
        print("url")
        print(url)

        try:
            response = requests.get(url)
            response.raise_for_status()  # Si la solicitud no es exitosa, lanzará una excepción
            data = response.json()

            for datos in data['items']:

                titulo = datos['volumeInfo']['title']
                autor = datos['volumeInfo'].get('authors', ['Desconocido'])
                fecha = datos['volumeInfo'].get('publishedDate', ['Desconocida'])
                paginas = datos['volumeInfo'].get('pageCount', ['Desconocida'])
                descripcion = datos['volumeInfo'].get('description', ['Desconocida'])
                if 'imageLinks' in datos['volumeInfo']:
                    imagen = datos['volumeInfo']['imageLinks'].get('thumbnail', 'Desconocida')
                else:
                    imagen = 'Desconocida'

                print(f"Título: {titulo}")
                print(f"Autor: {autor}")
                print(f"Fecha de publicación: {fecha}")
                print(f"Número de páginas: : {paginas}")
                print(f"Descripción: {descripcion}")
                print(f"Imagen: {imagen}")

            return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print("Error al realizar la solicitud:", e)
            return Response({"status": "error", "status":status.HTTP_400_BAD_REQUEST})


