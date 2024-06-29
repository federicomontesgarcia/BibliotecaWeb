from django.shortcuts import render
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

from django.shortcuts import render
from rest_framework.views import APIView
import requests
from rest_framework import status

class LibrosViews(APIView):

    def get(self, request, clave_api='AIzaSyCIUpw80bNcmyZZmVemB49yQcrViWjVvjs'):
    
        libro = request.GET.get('libro', '')
        autor = request.GET.get('autor', '')
        
        query = libro
        if autor:
            query += f'+inauthor:{autor}'

        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={clave_api}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Si la solicitud no es exitosa, lanzará una excepción
            data = response.json()
            
            libros = []

            for datos in data.get('items', []):
                libro = {
                    'titulo': datos['volumeInfo']['title'],
                    'autor': datos['volumeInfo'].get('authors', ['Desconocido']),
                    'fecha': datos['volumeInfo'].get('publishedDate', 'Desconocida'),
                    'paginas': datos['volumeInfo'].get('pageCount', 'Desconocida'),
                    'descripcion': datos['volumeInfo'].get('description', 'Desconocida'),
                    'imagen': datos['volumeInfo'].get('imageLinks', {}).get('thumbnail', 'Desconocida')
                }
                libros.append(libro)

            return render(request, "buscadores/buscador.html", {"libros": libros})

        except requests.exceptions.RequestException as e:
            print("Error al realizar la solicitud:", e)
            return render(request, "buscadores/buscador.html", {"error": "Error al realizar la solicitud"})


