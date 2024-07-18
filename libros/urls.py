from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('listado', views.libros, name="Libros"),
    path('save-book', views.save_book, name='grabarLibros'),
    path('eliminar_libro/<int:id_libro>/', views.eliminar_libro, name='eliminar_libro'),
    path('editar_libro/<int:id_libro>/', views.editar_libro, name='editar_libro'),
    path('save-book-edit', views.save_book_edit, name='grabar_editar_libro'),
    
    path('v1', views.LibroViews.as_view(), name="libro"),
    path('libro/<int:id>/', views.LibroViews.as_view()),
    path('autor/', views.AutorViews.as_view(), name="autor"),
    path('autor/<int:id>/', views.AutorViews.as_view()),
    path('genero/', views.GeneroViews.as_view()),
    path('genero/<int:id>/', views.GeneroViews.as_view(), name="genero"),
    path('books/', views.LibrosViews.as_view(), name="books"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
